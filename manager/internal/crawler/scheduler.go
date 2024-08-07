package crawler

import (
	"github.com/robfig/cron/v3"
	"log"
	"sync"
	"time"
)

// TODO move Job to models and create Job config type

// Job is a struct that represents a spider job
type Job struct {
	SpiderID        int
	SpiderCommand   string
	Status          int
	CreatedAt       time.Time
	IsRestartable   bool
	RestartDuration time.Duration
}

// Scheduler is a struct that schedules and manages spider jobs
type Scheduler struct {
	cron       *cron.Cron
	jobs       map[int]cron.EntryID
	jobQueue   []Job
	maxJobs    int
	activeJobs int
	mu         sync.Mutex
	queueMu    sync.Mutex
	stopChan   chan struct{}
}

var scheduler *Scheduler

func InitScheduler(maxJobs int) {
	scheduler = &Scheduler{
		cron:     cron.New(cron.WithSeconds()),
		jobs:     make(map[int]cron.EntryID),
		jobQueue: []Job{},
		maxJobs:  maxJobs,
		stopChan: make(chan struct{}),
	}
	scheduler.cron.Start()
}

func GetScheduler() *Scheduler {
	return scheduler
}

func (s *Scheduler) runJob(project, spider string) {
	s.mu.Lock()
	s.activeJobs++
	s.mu.Unlock()

	response, err := ScheduleSpider(project, spider)
	if err != nil {
		log.Printf("Failed to schedule spider %s: %v", spider, err)
	} else {
		log.Printf("Scheduled spider %s with job ID %s", spider, response.JobID)
	}

	s.mu.Lock()
	s.activeJobs--
	s.mu.Unlock()

	s.checkQueue()
}

func (s *Scheduler) checkQueue() {
	s.queueMu.Lock()
	defer s.queueMu.Unlock()

	if s.activeJobs < s.maxJobs && len(s.jobQueue) > 0 {
		job := s.jobQueue[0]
		s.jobQueue = s.jobQueue[1:]
		go s.runJob(job.SpiderCommand, job.SpiderCommand)
	}
}

func (s *Scheduler) ScheduleSpider(spiderID int, cronExpr string, project, spider string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	job := func() {
		s.queueMu.Lock()
		s.jobQueue = append(s.jobQueue, Job{SpiderID: spiderID, SpiderCommand: spider})
		s.queueMu.Unlock()
		s.checkQueue()
	}

	id, err := s.cron.AddFunc(cronExpr, job)
	if err != nil {
		return err
	}

	s.jobs[spiderID] = id
	return nil
}

func (s *Scheduler) StopSpider(spiderID int, project, jobID string) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if id, ok := s.jobs[spiderID]; ok {
		s.cron.Remove(id)
		delete(s.jobs, spiderID)
	}

	if err := CancelJob(project, jobID); err != nil {
		log.Printf("Failed to cancel job %s: %v", jobID, err)
	}
}

func (s *Scheduler) ListScheduledSpiders(project string) (*JobStatusResponse, error) {
	return GetJobStatus(project)
}

func (s *Scheduler) Shutdown() {
	close(s.stopChan)
	s.cron.Stop()
	log.Println("Scheduler stopped")
}

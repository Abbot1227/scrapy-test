package crawler

import (
	"github.com/robfig/cron/v3"
	"log"
	"os/exec"
	"sync"
)

// Scheduler is used for scheduling
// spiders using cron
type Scheduler struct {
	cron *cron.Cron
	jobs map[int]cron.EntryID
	mu   sync.Mutex
}

var scheduler *Scheduler

// InitScheduler creates global cron scheduler
func InitScheduler() {
	scheduler = &Scheduler{
		cron: cron.New(cron.WithSeconds()),
		jobs: make(map[int]cron.EntryID),
	}
	scheduler.cron.Start()
}

// GetScheduler returns scheduler instance
func GetScheduler() *Scheduler {
	return scheduler
}

func (s *Scheduler) ScheduleSpider(spiderID int, cronExpr string, spiderCommand string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	job := func() {
		cmd := exec.Command("sh", "scripts/run_spider.sh", spiderCommand)
		if err := cmd.Run(); err != nil {
			log.Printf("Failed to run spider %d: %v", spiderID, err)
		}
	}

	id, err := s.cron.AddFunc(cronExpr, job)
	if err != nil {
		return err
	}

	s.jobs[spiderID] = id
	return nil
}

func (s *Scheduler) StopSpider(spiderID int) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if id, ok := s.jobs[spiderID]; ok {
		s.cron.Remove(id)
		delete(s.jobs, spiderID)
	}
}

func (s *Scheduler) ListScheduledSpiders() map[int]cron.EntryID {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.jobs
}

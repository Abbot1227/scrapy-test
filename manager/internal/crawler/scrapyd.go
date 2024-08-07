package crawler

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"spider-scheduler/internal/config"
)

// ScheduleJobRequest is the request body for Scrapyd's schedule.json endpoint
type ScheduleJobRequest struct {
	Project string `json:"project"`
	Spider  string `json:"spider"`
}

// ScheduleResponse is the response from Scrapyd's schedule.json endpoint
type ScheduleResponse struct {
	NodeName string `json:"node_name"`
	Status   string `json:"status"`
	JobID    string `json:"jobid"`
}

// ScheduleSpider is wrapper around Scrapyd's schedule.json endpoint
// that schedules a spider to run and returns the job status and ID
func ScheduleSpider(project, spider string) (*ScheduleResponse, error) {
	jobRequest := ScheduleJobRequest{Project: project, Spider: spider}
	jsonData, err := json.Marshal(jobRequest)
	if err != nil {
		return nil, err
	}

	// Send POST request to schedule spider
	resp, err := http.Post(fmt.Sprintf(
		"%s/schedule.json", config.AppConfig.Scrapyd.Addr),
		"application/json", bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var scheduleResp ScheduleResponse
	err = json.Unmarshal(body, &scheduleResp)
	if err != nil {
		return nil, err
	}

	return &scheduleResp, nil
}

// JobStatusResponse is the response from Scrapyd's status.json endpoint
type JobStatusResponse struct {
	NodeName string `json:"node_name"`
	Status   string `json:"status"`
	State    string `json:"currstate"`
}

// GetJobStatus is a wrapper around Scrapyd's status.json endpoint
// that returns the status of a job by its ID
func GetJobStatus(jobID string) (*JobStatusResponse, error) {
	resp, err := http.Get(fmt.Sprintf("%s/status.json?job=%s", config.AppConfig.Scrapyd.Addr, jobID))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var statusResp JobStatusResponse
	err = json.Unmarshal(body, &statusResp)
	if err != nil {
		return nil, err
	}

	return &statusResp, nil
}

// TODO finish CancelJob function later
// TODO add request and response types
func CancelJob(project, jobID string) error {
	req, err := http.NewRequest("POST", fmt.Sprintf("%s/cancel.json", config.AppConfig.Scrapyd.Addr), nil)
	if err != nil {
		return err
	}

	q := req.URL.Query()
	q.Add("project", project)
	q.Add("job", jobID)
	req.URL.RawQuery = q.Encode()

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("failed to cancel job: %s", resp.Status)
	}

	return nil
}

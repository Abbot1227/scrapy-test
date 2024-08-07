package handlers

import (
	"encoding/json"
	"net/http"
	"spider-scheduler/internal/crawler"
)

// scheduleSpiderHandler schedules a spider to run
func scheduleSpiderHandler(w http.ResponseWriter, r *http.Request) {
	var req crawler.ScheduleJobRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	resp, err := crawler.ScheduleSpider(req.Project, req.Spider)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(resp)
}

// getJobStatusHandler returns the status of a job by ID
func getJobStatusHandler(w http.ResponseWriter, r *http.Request) {
	jobID := r.URL.Query().Get("job")
	if jobID == "" {
		http.Error(w, "job id is required", http.StatusBadRequest)
		return
	}
	resp, err := crawler.GetJobStatus(jobID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(resp)
}

// cancelJobHandler cancels a job by its ID
func cancelJobHandler(w http.ResponseWriter, r *http.Request) {
	jobID := r.URL.Query().Get("job")
	if
}

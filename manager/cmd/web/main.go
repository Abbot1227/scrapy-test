package main

import (
	"github.com/go-chi/chi/v5"
	"log"
	"net/http"
	"spider-scheduler/internal/config"
)

type app struct {
	config config.Config
	server http.Server
	logger log.Logger
	// TODO add other fields
}

func main() {
	a := app{
		config: config.AppConfig,
	}
	config.MustLoad()

	r := chi.NewRouter()
	a.server = http.Server{
		Addr:    ":" + config.AppConfig.Server.Addr,
		Handler: r,
	}

	log.Fatal("listening on "+a.server.Addr, "\n", a.server.ListenAndServe())
}

package config

import (
	"github.com/spf13/viper"
	"log"
)

type Config struct {
	Server  ServerConfig
	Scrapyd ScrapydConfig
}

type ServerConfig struct {
	Addr string
}

type ScrapydConfig struct {
	Addr string
}

var AppConfig Config

func MustLoad() {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("config")

	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("failed to read config file: %v", err)
	}

	if err := viper.Unmarshal(&AppConfig); err != nil {
		log.Fatalf("failed to unmarshal config: %v", err)
	}
}

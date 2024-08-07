package middleware

import (
	"net/http"
)

const (
	username = "admin"
	password = "12345678"
)

func basicAuth(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		auth := r.Header.Get("Authorization")
		if auth == "" {
			w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
			http.Error(w, "Not Authorized", http.StatusUnauthorized)
			return
		}

	})
}

package main

import (
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"time"
)

type Article struct {
	SourceCode        string `json:"source_code" ,csv:"source_code"`
	Name              string `json:"name" ,csv:"name"`
	Slug              string `json:"slug" ,csv:"slug"`
	MainUrl           string `json:"main_url" ,csv:"main_url"`
	NewsUrl           string `json:"news_url" ,csv:"news_url"`
	LogoUrl           string `json:"logo_url" ,csv:"logo_url"`
	Type              string `json:"type" ,csv:"type"`
	Rank              string `json:"rank" ,csv:"rank"`
	ScrapeStatus      string `json:"scrape_status" ,csv:"scrape_status"`
	MainDivNews       string `json:"main_div_news" ,csv:"main_div_news"`
	Title             string `json:"title" ,csv:"title"`
	PublishedDate     string `json:"published_date" ,csv:"published_date"`
	NewsPageUrl       string `json:"news_page_url" ,csv:"news_page_url"`
	RelativeUrl       string `json:"relative_url" ,csv:"relative_url"`
	Summary           string `json:"summary" ,csv:"summary"`
	Tags              string `json:"tags" ,csv:"tags"`
	Author            string `json:"author" ,csv:"author"`
	ContentMainDiv    string `json:"content_main_div" ,csv:"content_main_div"`
	ContentParaPIfNot string `json:"content_para_P_if_not" ,csv:"content_para_P_if_not"`
	ContentParaPClass string `json:"content_para_P_class" ,csv:"content_para_P_class"`
	Notes             string `json:"notes" ,csv:"notes"`
}

func main() {
	start := time.Now()
	defer fmt.Println("Time elapsed: ", time.Since(start))

	var csvFileName, jsonFileName string
	flag.StringVar(&csvFileName, "csv", "urls.csv", "csv filename")
	flag.StringVar(&jsonFileName, "json", "urls.json", "json filename")
	flag.Parse()

	ReadCSV(csvFileName, jsonFileName)
}

func ReadCSV(csvFileName, jsonFileName string) {
	csvFile, err := os.Open(csvFileName)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer csvFile.Close()

	csvReader := csv.NewReader(csvFile)

	rows, err := csvReader.ReadAll()
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	if len(rows) == 0 {
		fmt.Println("No rows found")
		return
	}

	header := rows[0]
	var articles []Article

	for _, row := range rows[1:] {
		article := Article{}
		for i, col := range row {
			switch header[i] {
			case "source_code":
				article.SourceCode = col
			case "name":
				article.Name = col
			case "slug":
				article.Slug = col
			case "main_url":
				article.MainUrl = col
			case "news_url":
				article.NewsUrl = col
			case "logo_url":
				article.LogoUrl = col
			case "type":
				article.Type = col
			case "rank":
				article.Rank = col
			case "scrape_status":
				article.ScrapeStatus = col
			case "main_div_news":
				article.MainDivNews = col
			case "title":
				article.Title = col
			case "published_date":
				article.PublishedDate = col
			case "news_page_url":
				article.NewsPageUrl = col
			case "relative_url":
				article.RelativeUrl = col
			case "summary":
				article.Summary = col
			case "tags":
				article.Tags = col
			case "author":
				article.Author = col
			case "content_main_div":
				article.ContentMainDiv = col
			case "content_para_P_if_not":
				article.ContentParaPIfNot = col
			case "content_para_P_class":
				article.ContentParaPClass = col
			case "notes":
				article.Notes = col
			}
		}
		articles = append(articles, article)
	}

	jsonFile, err := os.Create(jsonFileName)
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer jsonFile.Close()

	encoder := json.NewEncoder(jsonFile)
	encoder.SetIndent("", "    ")
	err = encoder.Encode(articles)
	if err != nil {
		fmt.Println("Error encoding file:", err)
		return
	}

	fmt.Println("Data has been written to json file")
}

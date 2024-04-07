package fetch

import (
	"fmt"
	// "log"
	"regexp"
	"strconv"
)

const (
	pageUrl   = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/"
	userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0" +
		"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
)

type PageResult struct {
	Listings []string
}

type ListingFetcher struct {
	Fetcher[PageResult]
}

func (f *ListingFetcher) processResults() {
	for url, body := range f.urls_body {
		pattern := `<a\s+href="(/pl/oferta/[^"]+)">`
		re := regexp.MustCompile(pattern)
		matches := re.FindAllStringSubmatch(body, -1)

		pageResult := PageResult{}
		for _, match := range matches {
			fmt.Println("match:", match)
			pageResult.Listings = append(pageResult.Listings, match[1])
		}

		if len(pageResult.Listings) > 0 {
			f.results[url] = pageResult
		} else {
			f.chFailed <- url
		}
	}
}

func FetchListings(city string, pages int) map[string]PageResult {
	var pagesUrls []string
	for i := 1; i <= pages; i++ {
		url := pageUrl + city + "/?page=" + strconv.Itoa(i)
		pagesUrls = append(pagesUrls, url)
	}

	listingFetcher := ListingFetcher{Fetcher: *NewFetcher[PageResult](userAgent, pagesUrls)}
	listingFetcher.Fetch()
	listingFetcher.processResults()

	results := listingFetcher.GetResults()
	failedUrls := listingFetcher.GetFailedUrls()

	if len(failedUrls) > 0 {
		fmt.Println("Could not fetch the following urls:", failedUrls)
		// log.Println("Could not fetch the following urls:", failedUrls)
	}

	return results
}

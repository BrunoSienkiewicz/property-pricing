package types

type Listing struct {
	Info     ListingInfo
	Location ListingLocation
	Features ListingFeatures
}

type ListingInfo struct {
	Title         string
	Price         string
	PricePerMeter string
	Area          string
	Market        string
	Url           string
}

type ListingLocation struct {
	City      string
	Region    string
	Latitude  string
	Longitude string
}

type ListingFeatures struct {
	Features map[string]string

	Extras    []string
	Media     []string
	Security  []string
	Equipment []string
}

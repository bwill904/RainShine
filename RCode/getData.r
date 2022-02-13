
# function that calls classes
getWUData = function(pythonPath, granularity, state, city, dates) {
  
  # setup python connection and test that it works
  tryCatch(reticulate::use_python(pythonPath), 
           error = function(e) message("Python path is incorrect. Make sure the path is pointing to the .exe file.")
  )
  Sys.setenv(PYTHONPATH = "./PythonCode")
  reticulate::use_python(pythonPath)
  
  # formatting for passing to python function
  state = tolower(state)
  city = tolower(city)
  
  dfStations = read.csv("./Data/Stations.csv", stringsAsFactors = FALSE)
  dfStations[, c("State", "StateAbbrev", "City")] = sapply(dfStations[, c("State", "StateAbbrev", "City")], tolower)
  
  # state checking
  if (!state %in% c(unique(dfStations$State), unique(dfStations$StateAbbrev))) {
    return("Weather data not available for input state.")
  } else if (state %in% unique(dfStations$State)) {
    state = unique(dfStations$StateAbbrev[dfStations$State == state])
  }
    
  # city checking
  if (!city %in% unique(dfStations$City[dfStations$StateAbbrev == state])) {
    return("Weather data not available for input city.")
  }
  
  # dates check
  if (!lubridate::is.Date(dates)) return("Dates provided are not in date format.")
  if (granularity == "monthly") { # monthly data
    dates = unique(format(dates, "%Y-%m"))
  } else {
    return("Only monthly data is available currently. Please define 'monthly' as the granularity.")
  }
  
  # scrape data from wunderground
  pyScraper = reticulate::import('wunderground_scraper')
  dfData = pyScraper$scraper(pyScraper$getURL(dfStations, city, state), dates)
  
  return(dfData)
}

pythonPath = "C:/Users/bwill/anaconda3/python.exe"
granularity = "monthly"
state = "Georgia"
city = "atlanta"
dates = seq.Date(as.Date("2015-01-01"), as.Date("2015-12-01"), 'month')


df = getWUData(pythonPath, granularity, state, city, dates)

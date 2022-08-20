# function that calls classes
#' Title Get Weather Underground Data
#'
#' @param chromeDir Path for chrome executable file.
#' @param granularity Output granularity, currently only 'monthly' is available.
#' @param state US state of desired location.
#' @param city US city for desired location.
#' @param dates Desired date vector. Must be in date format.
#'
#' @return Dataframe object with historical weather data.
#' @export
#'
#' @examples getWUDataR(pythonPath = 'C:/Users/bwill/anaconda3/python.exe', granularity = 'monthly', state = 'GA', 
#' city = 'Atlanta', dates = as.Date(c('2021-01-01', '2021-02-01')))

getWUUrl <- function(granularity, station, dates) {
  
  if (tolower(granularity) == "monthly") {
    url <- paste0("https://www.wunderground.com/history/monthly/", station, "/date/", format(dates, "%Y-%m"))
  } else if (tolower(granularity) == "daily") {
    url <- paste0("https://www.wunderground.com/history/daily/", station, "/date/", format(dates, "%Y-%m-%d"))
  } else return("Please select monthly or daily granularity.")
  
  return(url)
}

granularity = "daily"
state = "Georgia"
city = "atlanta"
dates = seq.Date(as.Date("2015-01-01"), as.Date("2015-01-01"), 'month')
dirChrome = "C:/Program Files/Google/Chrome/Application/"

getWUData <- function(dirChrome = "C:/Program Files/Google/Chrome/Application/", granularity, state, city, dates) {
  
  require (dplyr)
  
  # setup remote driver
  if (dir.exists(dirChrome) | "chrome.exe" %in% list.files(dirChrome)) { # check chrome is installed
    vecDir <- list.dirs(dirChrome, recursive = FALSE, full.names = FALSE)
    chromeDriverVersion <- max(vecDir[vecDir != "SetupMetrics"])
  } else chromeDriverVersion <- "latest"
  
  driver <- RSelenium::rsDriver(browser=c("chrome"), chromever = '103.0.5060.53', check = TRUE)
  remote_driver <- driver[["client"]]
  
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
  if (!inherits(dates, 'Date')) return("Dates provided are not in date format.")
  
  station <- dfStations$Airport[dfStations$StateAbbrev == state & dfStations$City == city]
  
  # scrape data from wunderground
  remote_driver$navigate(url = getWUUrl(granularity, station, dates))
  
  if (granularity == "daily") {
    # determine first element in table (going to be a time) 
    htmlData <- remote_driver$findElements(using = "css", value = "tr")
    tableColumns <- sapply(htmlData, function(x) x$getElementText()) %>% .[grep("Time\nTemperature", .)] %>% strsplit("\\n") %>% unlist()
    firstTableElement <- sapply(htmlData, function(x) x$getElementText()) %>% .[grep("Time\nTemperature", .)+1] %>% unlist() %>% strsplit(., "M ")
    firstTableElement <- paste0(firstTableElement[[1]][1], "M")
    
    # create data table
    htmlData <- remote_driver$findElements(using = "css", value = "tr td")
    vecData <- sapply(htmlData, function(x) x$getElementText()) %>% .[match(firstTableElement, .):length(.)] %>% unlist()
    dfData <- data.frame(stat = tableColumns, value = vecData, stringsAsFactors = FALSE) %>% 
      dplyr::mutate(period = sort(rep(1:(length(vecData)/length(tableColumns)), length(tableColumns))))
    
    # remove units from values and put them in metric names
    dfData$stat <- sapply(1:nrow(dfData), function(i) ifelse(dfData$stat[i] %in% c("Time", "Condition", "Wind"), dfData$stat[i], 
                                                      paste0(dfData$stat[i], " (", unlist(strsplit(dfData$value[i], " "))[2], ")")))
    dfData$value <- sapply(1:nrow(dfData), function(i) ifelse(dfData$stat[i] %in% c("Time", "Condition", "Wind"), dfData$value[i], 
                                                             unlist(strsplit(dfData$value[i], " "))[1]))
    
    dfData <- dfData %>% tidyr::spread(stat, value) %>% 
      dplyr::mutate(Station = station, Date = dates) %>% dplyr::select(-period) %>% tidyr::gather(Metric, Value, -c(Station, Date, Time)) %>%
      dplyr::select(c(Station, Date, Time, Metric, Value))
    
  } else if (granularity == "monthly") {
    
    htmlData <- remote_driver$findElements(using = "css", value = "tr td")
    vecData <- sapply(htmlData, function(x) x$getElementText()) %>% .[grep("Time", .):length(.)] %>% unlist()
    vecColnames <- c("Date", vecData[2:(grep("\\n", vecData)[1]-1)])
    vecData <- vecData %>% .[grepl("\\n", .)]
    
    dfData <- data.frame()  
    for (i in 1:length(vecData)) {
      vecTemp <- vecData[i] %>% strsplit("\\n") %>% unlist()
      
      if (vecTemp[1] == format(dates, "%b")) { # check if a date column
        vecDate <- as.Date(paste(format(dates, "%Y"), format(dates, "%m"), vecTemp[2:length(vecTemp)], sep = "-"))
      } else {
        tempColnames <- vecTemp[1] %>% strsplit(" ") %>% unlist()
        dfString <- vecTemp[-1] %>% strsplit(" ") %>% do.call(rbind, .) %>% as.numeric() %>% matrix(ncol = length(tempColnames)) %>% 
          as.data.frame() %>% `colnames<-`(tempColnames) %>% tidyr::gather(Stat, Value) %>% 
          dplyr::mutate(Metric = vecColnames[i], Date = rep(vecDate, length(tempColnames)))
        dfData <- rbind(dfString, dfData)
      }
    }
    dfData <- dfData %>% dplyr::mutate(Station = station) %>% dplyr::select(Station, Date, Metric, Stat, Value)
  }
  
  remote_driver$close()
  system("taskkill /im java.exe /f", intern=FALSE, ignore.stdout=FALSE) # close the port
  
  return(dfData) 
}


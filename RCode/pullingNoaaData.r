
library(tidyverse)
config <- config::get()

# get noaa stations
if (!file.exists("./Data/dfStations.rds")) {
  dfStations <- rnoaa::ghcnd_stations()
  saveRDS(dfStations, "./Data/dfStations.rds")
} else dfStations <- readRDS("./Data/dfStations.rds")

# get station data for US stations
dfStations <- dfStations %>% dplyr::filter(!state %in% c("", "AK", "HI") & toupper(substr(id, 1, 2)) == "US" & gsn_flag == "GSN")

# plot stations visually
my_sf <- sf::st_as_sf(dfStations, coords = c('longitude', 'latitude'))
my_sf <- sf::st_set_crs(my_sf, 4326)
ggplot2::ggplot(my_sf) + ggplot2::geom_sf()

if (!file.exists("./Data/dfStationData.rds")) {
  if (!file.exists("./Data/lstStationData.rds")) {
    lstData <- list()
    for (station in unique(dfStations$id)) {
      lstData[[station]] <- rnoaa::ghcnd_search(stationid = station)
    }
    saveRDS(lstData, "./Data/lstStationData.rds")
  } else lstData <- readRDS("./Data/lstStationData.rds")
  
  
  # convert data to one dataframe
  dfData <- do.call("rbind", lapply(lstData, function(x) {
    for(output in names(x)) {
      dfTemp <- tidyr::gather(x[[output]], metric, value, -c(id, date, mflag, qflag, sflag))
      if (output == names(x)[1]) {
        dfOutput <- dfTemp
      } else dfOutput <- dplyr::bind_rows(dfOutput, dfTemp)
    }
    return(dfOutput)
  })
  )
  saveRDS(dfData, "./Data/dfStationData.rds")
}

dfData <- readRDS("./Data/dfStationData.rds")


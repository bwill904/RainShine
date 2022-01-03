
# main class
weatherData <- R6::R6Class(
 classname = "main",
 public = list(
  getData = function(source, dates) {
    return("please select a data source, either 'WU' or 'NOAA'.")
  }
 ), 
 private = list(
  source = "none",
  location = "Atlanta",
  dates = Sys.Date()
 )
)

NOAAData <- R6::R6Class(
 classname = "NOAA",
 public=  list(
   getData = function(source, location, dates) {
     # figure out how to pull NOAA data
   }
 ),
 private = list(
   source = "NOAA",
   location = "Atlanta",
   dates = Sys.Date()
 )
)

WUData <- R6::R6Class(
  classname = "WU",
  public=  list(
    getData = function(source, location, dates) {
      # figure out how to pull WU data
    }
  ),
  private = list(
    source = "WU",
    location = "Atlanta",
    dates = Sys.Date()
  )
)
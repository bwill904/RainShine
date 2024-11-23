
library(dplyr)

lstGIQueue <- list()

# pulling data from the SPP GI queue
dfSPPTypeMap <- list("None" = "Active", 
                  "FACILITY STUDY STAGE" = "Active", 
                  "IA PENDING" = "Active", 
                  "WITHDRAWN" = "Withdrawn", 
                  "DISIS STAGE" = "Active", 
                  "IA FULLY EXECUTED/ON SCHEDULE" = "Active", 
                  "TERMINATED" = "Withdrawn",                           
                  "IA FULLY EXECUTED/COMMERCIAL OPERATION" = "Operational",
                  "IA FULLY EXECUTED/ON SUSPENSION" = "Active")

dfSPPQueue <- read.csv("https://opsportal.spp.org/Studies/GenerateSummaryCSV", stringsAsFactors = F, skip = 1)
dfSPPQueue <- dfSPPQueue %>% dplyr::mutate(StartDate = ifelse(Commercial.Operation.Date == "", 
                                     Replacement.Generator.Commercial.Op.Date, Commercial.Operation.Date), 
                                     Type = sapply(Status, function(x) dfTypeMap[[x]])) %>% 
  dplyr::select(StartDate, Status = Type, Nearest.Town.or.County, State, TO.at.POI, Generation.Type, 
                Fuel.Type, Substation.or.Line, SummerMW = MAX.Summer.MW, WinterMW = MAX.Winter.MW) %>% 
  dplyr::mutate(StartDate = as.Date(StartDate, "%m/%d/%Y"))

# pulling data from MISO GI Queue
dfMISOQueue <- read.csv("C:/Users/Brandon Williams/Documents/RainShine/Data/GI Queue/2024-11-23/MISO GI Interactive Queue.csv", stringsAsFactors = F)

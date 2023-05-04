



a bad number_of_events
  10522 #--> project: /juno/res/ci/voyager/argos/./13792/1.1.2/20221123_16_45_510150 running sample:  s_C_PAE3NL_P002_d02


Quitting from lines 20-22 (report_sample_level.Rmd)                             
  10536 Error in `left_join()`:                                                         
  10537 ! Can't join on `x$Chromosome` x `y$Chromosome` because of incompatible         
  10538   types.                                                                        
  10539 ℹ `x$Chromosome` is of type <double>>.                                          
  10540 ℹ `y$Chromosome` is of type <character>>.                                       
  10541 Backtrace:                                                                      
  10542  1. global load_data(params$argosDir, params$sampleID)                          
  10543  5. dplyr:::left_join.data.frame(., oncoKb$dat, by = oncoKbKey)           
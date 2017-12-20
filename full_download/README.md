### Downloading filings from edgar - Full download

#### Configuration

  - Configuration File [config.cfg](config.cfg)
  - Items
      + archive -> filters:
        Each part of the filter is separated by a semi colon. Every filter
       part contains four parts
       	    - Year of filing
	    - Quarter of filing
	    - Type of filing
	    - cik code
      + Thus for getting all the 8-K filings of 1050122 from 2002 Quarter 3, the filter will be
	     ``` 2002:QTR3:8:-K:1050122  ```
      + If last two fields of the filter are kept empty which the crawler will collect all filings from 2002, QTR3.
      + If the last three fields are kept empty, the crawler will collect all filings from 2002.
      + Multiple filters like this has to be separated by a semicolon. A typical filter would look like
        	 	 ``` 2002:QTR3::1050122;2017:QTR4:10-Q:1588014;2016:QTR2:8-K: ```
		
   - For running the code
	     
       1. configure the filters
       2. Run the code by ``` ipython downloader.py ```	  
		    
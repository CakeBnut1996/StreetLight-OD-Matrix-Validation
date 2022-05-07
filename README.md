# Generate OD Demand from StreetLight Inside

Step 1: Input your Taffic Analysis Zone shapefile

![image](https://user-images.githubusercontent.com/46463367/167269684-1834220f-18fc-4c49-882e-fdcddc7f73ca.png)

Step 2: Set Calibration links

StreetLight uses AADT estimates to scale the STL sample trip count to the estimated counts. 
- Number of zones
- Location of zones
- How to scale

![image](https://user-images.githubusercontent.com/46463367/167269688-2b1dcb80-e8db-471c-bd6c-eeb2c7f18685.png)

Step 3: Set time and day to generate different scenarios. Here three scenarios are generated:
- School: Mar, Apr; Sep, Oct. Spring recess was excluded
- Snowbirds: Nov, Dec, Jan
- Summer (School Break): June, Jul, Aug. Days after Aug.20 (school starts) were excluded.

![image](https://user-images.githubusercontent.com/46463367/167269728-7df4bbf5-c366-4fa6-9329-9aac717d88cc.png)

# See the Generated StreetLight
Sample of Raw OD Data*: 1104 zones
*If the values for an OD pair for a specific time period (e.g. Early AM) are below StreetLight's significance threshold, no results will be shown in the CSV files.

<img width="561" alt="image" src="https://user-images.githubusercontent.com/46463367/167269794-685e57e4-fae2-4a1d-916e-8b33465b8a02.png">

# Convert StreetLight wide format of OD matrix to traffic simulation input format
Step 1: Raw OD Table Cleaning (Figure 1)
- Keep weekday (Mon-Thu)) OD traffic
- Complete OD data in order to make Zone ID continuous. Missing data are given NAs.
- Sort based on start hour, origin ID, destination ID

Step 2: Conversion to traffic simulation input format (Figure 2)
- Create an empty .dat file
- Write # of time intervals, growth factors,  start time of each interval in minutes
- For each row in raw OD table (.csv):
  - If the line number is multiple of 1104^2 (OD table for one hour):
  - Write “Start Time = XXX”
    - Write values from the column - calibrated OD traffic 
  - If reaching 6 values a line or the line number is multiple of 1104 (new origin ID)
    - Start a new line 
   
<img width="557" alt="image" src="https://user-images.githubusercontent.com/46463367/167269904-27807561-400b-466c-85b9-5bfe435c86b1.png">


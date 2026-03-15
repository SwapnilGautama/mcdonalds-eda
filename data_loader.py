import pandas as pd
import numpy as np

def load_menu():
    data = [
        ["Breakfast","Egg & Cheese Muffin",112,290,14,13.0,7.0,0.2,244,28,2,2,620],
        ["Breakfast","Sausage McMuffin",112,273,16,11.0,5.7,0.2,50,28,2,2,950],
        ["Breakfast","Sausage & Egg McMuffin",157,355,22,17.0,7.9,0.2,277,29,2,2,1020],
        ["Breakfast","Veg McMuffin",119,299,10,12.0,7.2,0.2,21,38,3,3,1000],
        ["Breakfast","Veg Supreme Muffin",139,299,7,13.0,5.2,0.2,11,39,4,4,960],
        ["Breakfast","Bacon, Egg & Cheese Bagel",247,590,29,29.0,12.0,0.5,255,57,7,3,1360],
        ["Breakfast","Bacon, Egg & Cheese Bagel with Egg Whites",247,520,30,24.0,10.0,0.5,25,57,7,3,1320],
        ["Breakfast","Big Breakfast (Large Biscuit)",345,740,33,48.0,16.0,0.5,535,51,3,4,1560],
        ["Breakfast","Big Breakfast (Regular Biscuit)",290,690,33,45.0,16.0,0.5,535,44,3,3,1530],
        ["Breakfast","Big Breakfast with Egg Whites (Large Biscuit)",345,650,35,40.0,14.0,0.5,305,52,3,4,1430],
        ["Breakfast","Big Breakfast with Hotcakes (Large Biscuit)",520,1090,36,56.0,18.0,0.5,535,116,45,4,1920],
        ["Breakfast","Big Breakfast with Hotcakes (Regular Biscuit)",465,1040,35,53.0,17.0,0.5,535,109,45,4,1890],
        ["Breakfast","Big Breakfast with Hotcakes and Egg Whites (Large Biscuit)",520,1000,38,48.0,16.0,0.5,305,117,45,4,1790],
        ["Breakfast","Big Breakfast with Hotcakes and Egg Whites (Regular Biscuit)",465,950,37,44.0,15.0,0.5,305,110,45,4,1760],
        ["Breakfast","Steak, Egg & Cheese Bagel",246,670,38,35.0,12.0,0.5,295,57,7,3,1510],
        ["Breakfast","Egg McMuffin",136,300,17,12.0,5.0,0.0,260,31,3,2,760],
        ["Breakfast","Hotcakes",228,580,9,16.0,3.5,0.0,20,102,44,3,680],
        ["Breakfast","Hotcakes and Sausage",274,780,20,33.0,10.0,0.0,70,102,44,3,1010],
        ["Breakfast","Sausage Biscuit",130,430,11,27.0,11.0,0.5,35,34,3,1,1080],
        ["Breakfast","Sausage Biscuit with Egg",185,530,19,34.0,13.0,0.5,255,35,3,1,1310],
        ["Chicken & Fish","Artisan Grilled Chicken Sandwich",213,380,37,7.0,1.5,0.0,95,44,11,3,960],
        ["Chicken & Fish","Buttermilk Crispy Chicken Sandwich",218,530,27,22.0,4.0,0.0,60,55,10,3,1110],
        ["Chicken & Fish","Chicken McNuggets (4 piece)",64,190,10,12.0,2.0,0.0,25,11,0,0,360],
        ["Chicken & Fish","Chicken McNuggets (6 piece)",96,280,15,18.0,3.0,0.0,40,17,0,0,540],
        ["Chicken & Fish","Chicken McNuggets (10 piece)",160,470,25,30.0,5.0,0.0,65,28,0,0,900],
        ["Chicken & Fish","Chicken McNuggets (20 piece)",319,940,50,60.0,10.0,0.0,130,57,0,0,1800],
        ["Beef & Pork","Big Mac",200,530,25,26.0,10.0,1.0,80,46,9,3,960],
        ["Beef & Pork","Double Big Mac",268,680,37,38.0,13.0,1.5,120,47,9,3,1120],
        ["Beef & Pork","Quarter Pounder with Cheese",198,530,30,26.0,13.0,1.5,100,43,10,2,1090],
        ["Beef & Pork","McDouble",155,390,23,18.0,8.0,1.0,70,34,7,2,840],
        ["Beef & Pork","Hamburger",105,250,12,8.0,3.5,0.5,30,32,6,1,500],
        ["Beef & Pork","Cheeseburger",116,300,15,12.0,6.0,0.5,40,32,6,1,750],
        ["Beef & Pork","Double Cheeseburger",171,440,25,22.0,11.0,1.0,80,34,7,2,1050],
        ["Beef & Pork","McRib",228,490,22,23.0,9.0,0.0,70,53,10,3,980],
        ["Salads","Side Salad",87,20,1,0.0,0.0,0.0,0,4,2,1,10],
        ["Salads","Premium Southwest Salad (Grilled Chicken)",338,350,37,11.0,3.5,0.0,70,27,8,7,1070],
        ["Salads","Premium Bacon Ranch Salad (Grilled Chicken)",330,230,33,8.0,4.0,0.0,90,12,4,3,710],
        ["Salads","Premium Caesar Salad (Grilled Chicken)",272,190,30,5.0,2.5,0.0,75,14,4,3,780],
        ["Snacks & Sides","French Fries (Small)",71,230,3,11.0,1.5,0.0,0,29,0,3,160],
        ["Snacks & Sides","French Fries (Medium)",117,340,4,16.0,2.0,0.0,0,44,0,4,230],
        ["Snacks & Sides","French Fries (Large)",177,510,7,24.0,3.0,0.0,0,66,1,6,350],
        ["Snacks & Sides","Apple Slices",73,15,0,0.0,0.0,0.0,0,4,3,0,0],
        ["Desserts","Soft Baked Chocolate Chip Cookie",33,160,2,8.0,4.0,0.0,15,22,13,1,90],
        ["Desserts","McFlurry with Oreo Cookies",348,690,15,24.0,15.0,0.5,65,101,74,1,280],
        ["Desserts","McFlurry with M&Ms",337,690,15,24.0,14.0,0.5,65,107,81,0,210],
        ["Desserts","Baked Apple Pie",77,250,2,13.0,6.0,0.0,0,32,13,1,170],
        ["Desserts","Strawberry & Creme Pie",78,290,3,16.0,9.0,0.5,10,35,17,1,170],
        ["Hot Beverages","Brewed Coffee (Small)",354,0,0,0.0,0.0,0.0,0,0,0,0,5],
        ["Hot Beverages","Brewed Coffee (Medium)",473,0,0,0.0,0.0,0.0,0,0,0,0,5],
        ["Hot Beverages","Cappuccino (Small)",12,60,4,2.5,1.5,0.0,10,6,5,0,70],
        ["Hot Beverages","Latte (Medium)",354,130,8,5.0,3.0,0.0,20,13,12,0,130],
        ["Hot Beverages","Hot Chocolate (Small)",384,370,11,12.0,9.0,0.5,40,58,50,2,170],
        ["Cold Beverages","Coca-Cola (Small)",355,140,0,0.0,0.0,0.0,0,38,38,0,40],
        ["Cold Beverages","Coca-Cola (Large)",887,310,0,0.0,0.0,0.0,0,86,86,0,90],
        ["Cold Beverages","Sprite (Medium)",621,200,0,0.0,0.0,0.0,0,54,54,0,90],
        ["Cold Beverages","Orange Juice (Small)",355,150,2,0.0,0.0,0.0,0,36,33,0,25],
        ["Cold Beverages","Minute Maid Apple Juice",200,90,0,0.0,0.0,0.0,0,23,22,0,15],
        ["Smoothies & Shakes","Chocolate Shake (Small)",354,530,13,15.0,10.0,0.5,50,82,67,1,220],
        ["Smoothies & Shakes","Vanilla Shake (Small)",354,520,12,14.0,9.0,0.5,50,80,67,0,200],
        ["Smoothies & Shakes","Strawberry Shake (Small)",354,510,12,14.0,9.0,0.5,50,79,67,0,200],
        ["Smoothies & Shakes","Strawberry Banana Smoothie (Small)",326,210,2,0.5,0.0,0.0,5,48,44,2,30],
        ["Smoothies & Shakes","Mango Pineapple Smoothie (Small)",326,210,1,0.5,0.0,0.0,5,50,46,2,30],
        ["Nuggets","Chicken McNuggets (40 piece)",638,1880,87,120.0,20.0,0.0,260,113,0,0,3600],
        ["Nuggets","Chicken McNuggets (50 piece)",798,2350,109,150.0,25.0,0.0,325,141,0,0,4500],
        ["Condiments","Ketchup Packet",9,10,0,0.0,0.0,0.0,0,2,2,0,90],
        ["Condiments","Mustard Packet",5,5,0,0.0,0.0,0.0,0,0,0,0,55],
        ["Condiments","Ranch Dipping Sauce",45,200,1,21.0,3.0,0.0,10,3,2,0,340],
        ["Sandwiches and Wraps","Premium Grilled Chicken Classic Sandwich",213,350,28,9.0,2.0,0.0,70,42,8,2,820],
        ["Sandwiches and Wraps","Premium Crispy Chicken Classic Sandwich",213,510,26,22.0,3.5,0.0,60,50,8,2,1060],
        ["Sandwiches and Wraps","Premium Bacon Ranch Salad with Crispy Chicken",358,510,27,25.0,6.0,0.0,75,43,9,5,1130],
        ["Chicken Wings","Chicken McBites (Snack Size)",90,250,13,16.0,2.5,0.0,30,14,0,0,610],
        ["Chicken Wings","Chicken McBites (Regular)",180,500,26,32.0,5.0,0.0,60,27,0,0,1220],
        ["New Products","Mighty Wings",87,200,14,14.0,3.0,0.0,50,9,0,1,440],
        ["New Products","Chicken Selects (3 piece)",135,400,26,24.0,4.0,0.0,55,23,0,0,630],
    ]
    cols = ["Category","Item","Serve_Size","Energy","Protein","Total_Fat",
            "Saturated_Fat","Trans_Fat","Cholestrol","Carbohydrates","Sugars",
            "Dietary_Fibre","Sodium"]
    df = pd.DataFrame(data, columns=cols)
    df["Nutritious"] = df["Protein"] + df["Dietary_Fibre"]
    df["Non_Nutritious"] = df["Total_Fat"] + df["Saturated_Fat"] + df["Trans_Fat"] + df["Cholestrol"]
    df["Grilled"] = df["Item"].str.contains("Grilled", case=False, na=False)
    return df


def load_stores():
    data = [
        ["23149-228271","Banjara Hills","Joint Venture","Hyderabad","AP","IN",78.45,17.42,2.117,0.172,1.655,0.907,0.748,34,3979,"Egg & Cheese Muffin"],
        ["23191-228548","Kukatpally","Joint Venture","Hyderabad","AP","IN",78.39,17.48,1.059,0.055,0.896,0.454,0.442,25,1156,"Sausage McMuffin"],
        ["23193-228546","Madhapur","Joint Venture","Hyderabad","AP","IN",78.39,17.43,4.505,0.664,2.864,1.931,0.934,54,10347,"Sausage & Egg McMuffin"],
        ["23180-228545","Jubilee Hills","Joint Venture","Hyderabad","AP","IN",78.42,17.42,3.406,0.398,2.394,1.460,0.935,45,7415,"Veg McMuffin"],
        ["24457-238129","Hi-Tech City","Joint Venture","Hyderabad","AP","IN",78.38,17.45,7.333,1.657,3.395,3.143,0.252,77,17887,"Veg Supreme Muffin"],
        ["23293-229025","JP Nagar","Joint Venture","Bangalore","KA","IN",77.59,12.91,1.001,0.050,0.851,0.429,0.422,25,1002,"Sausage McMuffin"],
        ["21764-215225","Pitampura","Joint Venture","New Delhi","DL","IN",77.15,28.69,1.305,0.076,1.085,0.559,0.526,27,1814,"Veg McMuffin"],
        ["21816-215552","Malleswaram - Orion Mall","Joint Venture","Bangalore","KA","IN",77.56,13.01,1.777,0.127,1.426,0.761,0.664,31,3071,"Egg & Cheese Muffin"],
        ["20778-207865","Bandra West - Chapel road","Joint Venture","Mumbai","MH","IN",72.83,19.05,1.871,0.139,1.491,0.802,0.689,32,3323,"Sausage McMuffin"],
        ["22572-222668","Greater Kailash 2","Joint Venture","New Delhi","DL","IN",77.24,28.53,9.561,2.751,3.125,4.097,-0.972,96,23828,"4 piece Chicken Nuggets"],
        ["27717-248629","Hauz Khas","Joint Venture","New Delhi","DL","IN",77.19,28.55,1.897,0.142,1.508,0.813,0.695,32,3390,"Sausage McMuffin"],
        ["21606-213485","Koramangala","Joint Venture","Bangalore","KA","IN",77.61,12.94,2.035,0.160,1.601,0.872,0.729,34,3706,"Egg & Cheese Muffin"],
        ["19363-201204","Saket","Joint Venture","New Delhi","DL","IN",77.22,28.53,2.094,0.168,1.640,0.897,0.743,34,3853,"Egg & Cheese Muffin"],
        ["17857-186566","Goregaon East - Oberoi Mall","Joint Venture","Mumbai","MH","IN",72.86,19.17,2.101,0.169,1.645,0.901,0.744,34,3889,"Egg & Cheese Muffin"],
        ["19514-197404","Indira Gandhi Intl Arpt-T3","Joint Venture","New Delhi","DL","IN",77.10,28.56,9.686,2.821,3.092,4.151,-1.060,97,24162,"Large Fries"],
        ["19530-197407","Bandra East - FIFC","Joint Venture","Mumbai","MH","IN",72.87,19.07,9.918,2.953,3.025,4.251,-1.225,99,24780,"McFloat Fanta"],
        ["20457-205766","Thane West - Korum Mall","Joint Venture","Mumbai","MH","IN",72.97,19.20,9.850,2.914,3.045,4.221,-1.176,98,24599,"Kinley Water"],
        ["21743-215051","Church Street","Joint Venture","Bangalore","KA","IN",77.61,12.97,9.754,2.860,3.073,4.180,-1.108,97,24344,"Regular Coca-Cola"],
        ["23292-229027","CST Intl-T2 Arrival","Joint Venture","Mumbai","MH","IN",72.87,19.10,1.097,0.058,0.926,0.470,0.456,25,1258,"Sausage & Egg McMuffin"],
        ["76725-102051","Target Kansas City T-2222","Licensed","Kansas City","KS","US",-94.83,39.13,46.934,13.514,15.326,20.115,-4.789,141,23842,"Big Breakfast with Hotcakes (Large Biscuit)"],
        ["72668-65003","Super Target Tuscaloosa ST-1787","Licensed","Tuscaloosa","AL","US",-87.51,33.20,48.907,13.431,17.402,20.960,-3.559,146,22564,"Big Breakfast with Hotcakes and Egg Whites (Regular Biscuit)"],
        ["72121-3608","U of AL - Ferguson Cntr","Licensed","Tuscaloosa","AL","US",-87.55,33.21,44.138,12.745,14.334,18.916,-4.582,133,23919,"Big Breakfast with Hotcakes (Regular Biscuit)"],
        ["21772-214865","2001 L St","Company Owned","Washington","DC","US",-77.05,38.90,46.254,12.734,16.390,19.823,-3.433,139,22628,"Big Breakfast with Hotcakes (Large Biscuit)"],
        ["9706-96992","Champaign - 5th & Green","Company Owned","Champaign","IL","US",-88.23,40.11,48.424,12.536,18.908,20.753,-1.846,145,21052,"Big Breakfast with Hotcakes and Egg Whites (Large Biscuit)"],
        ["76740-99373","Target Cleveland South T-2228","Licensed","Cleveland","OH","US",-81.69,41.46,49.044,12.418,19.764,21.019,-1.255,147,20506,"Big Breakfast with Hotcakes and Egg Whites (Large Biscuit)"],
        ["6314-6908","Magazine & Washington","Company Owned","New Orleans","LA","US",-90.08,29.93,44.154,12.329,15.264,18.923,-3.659,133,23005,"Big Breakfast with Hotcakes (Regular Biscuit)"],
        ["2659-66300","State Rd 135 & Stonegate","Company Owned","Greenwood","IN","US",-86.16,39.63,46.584,12.325,17.605,19.965,-2.360,140,21599,"Big Breakfast with Hotcakes (Large Biscuit)"],
        ["25202-201748","Kroger Southwest Store #572","Licensed","Bartonville","TX","US",-97.13,33.08,41.786,12.145,13.396,17.908,-4.512,126,24101,"Premium Grilled Chicken Classic Sandwich"],
        ["76482-98011","Target Midwest City T-2061","Licensed","Midwest City","OK","US",-97.40,35.44,44.352,12.119,15.916,19.008,-4.532,134,24076,"Big Breakfast (Large Biscuit)"],
        ["10753-102015","19th & Telephone","Company Owned","Moore","OK","US",-97.50,35.32,49.681,4.066,38.749,21.292,17.457,149,4056,"Premium Grilled Chicken Classic Sandwich"],
        ["27316-246764","Fort Sill BX","Licensed","Fort Sill","OK","US",-98.40,34.67,49.416,5.617,35.081,21.178,13.903,148,7112,"Premium Grilled Chicken Classic Sandwich"],
        ["15847-160724","Target Gateway T-1401","Licensed","Brooklyn","NY","US",-73.87,40.65,48.779,5.765,34.146,20.905,13.240,146,7545,"Premium Grilled Chicken Classic Sandwich"],
        ["20344-204610","Target Fountain Hills T-1432","Licensed","Fountain Hills","AZ","US",-111.72,33.57,48.745,7.053,31.278,20.891,10.387,146,10091,"Premium Grilled Chicken Classic Sandwich"],
        ["9813-97844","JFK & McCain","Company Owned","North Little Rock","AR","US",-92.25,34.80,48.689,8.021,29.095,20.867,8.228,146,12015,"Premium Grilled Chicken Classic Sandwich"],
        ["13949-109207","SR 135 & Faith","Company Owned","Greenwood","IN","US",-86.16,39.61,48.570,2.887,40.275,20.816,19.459,145,1906,"Premium Grilled Chicken Classic Sandwich"],
        ["7381-1628","Elmwood Avenue","Company Owned","Buffalo","NY","US",-78.88,42.92,48.291,8.185,28.352,20.696,7.656,145,12471,"Premium Grilled Chicken Classic Sandwich"],
        ["3236-251306","Hwy 44 & Edgewood - Eagle","Company Owned","Eagle","ID","US",-116.33,43.69,38.210,11.449,11.494,16.376,-4.882,116,24964,"Chicken McNuggets (40 piece)"],
        ["73744-103865","Hy-Vee - Bettendorf #1","Licensed","Bettendorf","IA","US",-90.48,41.55,23.799,7.007,7.431,10.200,-2.768,75,24465,"Premium Crispy Chicken Classic Sandwich"],
        ["76916-131305","Target Wasilla T-2339","Licensed","Wasilla","AK","US",-149.41,61.58,40.710,11.895,12.912,17.447,-4.535,123,24250,"Premium Grilled Chicken Classic Sandwich"],
        ["18029-182674","Kroger Shreveport #539","Licensed","Shreveport","LA","US",-93.72,32.45,21.969,6.409,6.991,9.415,-2.424,69,24205,"Regular Coca-Cola"],
        ["11709-104595","Maumelle & Audubon","Company Owned","Maumelle","AR","US",-92.40,34.85,33.984,9.891,10.866,14.565,-4.882,116,24964,"Premium Grilled Chicken Classic Sandwich"],
        ["79622-104108","Safeway - Boring #521","Licensed","Damascus","OR","US",-122.46,45.42,19.283,3.393,11.048,8.264,2.783,62,13091,"Premium Grilled Chicken Classic Sandwich"],
        ["10612-101375","Cleveland & Owen K. Garriott","Company Owned","Enid","OK","US",-97.91,36.39,36.725,3.893,26.690,15.739,10.951,112,6377,"Premium Grilled Chicken Classic Sandwich"],
        ["3415-86784","9th & Garfield - Corvallis","Company Owned","Corvallis","OR","US",-123.26,44.58,38.106,8.172,18.605,16.331,2.273,116,16786,"Premium Grilled Chicken Classic Sandwich"],
        ["75221-94079","U of Cincinnati Student Life Ctr","Licensed","Cincinnati","OH","US",-84.51,39.13,37.755,2.670,30.370,16.181,14.190,115,2989,"Big Breakfast with Hotcakes (Large Biscuit)"],
        ["2420-201504","University Square","Company Owned","Cincinnati","OH","US",-84.52,39.13,22.264,2.298,16.319,9.542,6.777,70,6107,"Big Breakfast with Hotcakes and Egg Whites (Large Biscuit)"],
        ["19787-189469","Kroger - Cincinnati #428","Licensed","Cincinnati","OH","US",-84.51,39.16,15.004,3.169,7.432,6.430,1.002,50,16476,"Big Breakfast with Hotcakes (Regular Biscuit)"],
        ["2212-639","Mariemont/The Strand","Company Owned","Cincinnati","OH","US",-84.38,39.15,19.026,1.711,14.500,8.154,6.346,60,8235,"Big Breakfast with Hotcakes and Egg Whites (Regular Biscuit)"],
        ["10084-99523","Houston Levee & Winchester","Company Owned","Collierville","TN","US",-89.73,35.05,23.606,1.575,19.197,10.117,9.080,74,2605,"Big Breakfast with Hotcakes and Egg Whites (Large Biscuit)"],
        ["17746-178124","Paul Huff & I-75","Company Owned","Cleveland","TN","US",-84.86,35.21,41.815,11.164,15.582,17.921,-2.338,126,21829,"Big Breakfast with Hotcakes and Egg Whites (Large Biscuit)"],
        ["10170-96331","244 Ellendale Ave - Dallas","Company Owned","Dallas","OR","US",-123.31,44.93,28.751,7.268,11.612,12.322,4.342,88,14920,"Premium Grilled Chicken Classic Sandwich"],
        ["10052-99312","Robinson, Lafayette Plaza","Company Owned","Pittsburgh","PA","US",-80.18,40.45,24.401,4.027,14.566,10.461,4.105,75,8982,"Premium Grilled Chicken Classic Sandwich"],
    ]
    cols = ["Store_ID","Store_Name","Ownership_Type","City","State","Country",
            "Longitude","Latitude","Revenue","Profits","Selling_Price","Cost_Price",
            "Gross_Profit_Margin","Number_of_Employees","Customers","Best_Selling_Item"]
    return pd.DataFrame(data, columns=cols)


def load_merged():
    stores = load_stores()
    menu = load_menu()
    df = pd.merge(stores, menu, how="left", left_on="Best_Selling_Item", right_on="Item")
    df.drop(columns=["Item"], errors="ignore", inplace=True)
    df["Nutritious"] = df["Protein"].fillna(0) + df["Dietary_Fibre"].fillna(0)
    df["Non_Nutritious"] = (df["Total_Fat"].fillna(0) + df["Saturated_Fat"].fillna(0)
                            + df["Trans_Fat"].fillna(0) + df["Cholestrol"].fillna(0))
    df["Revenue_per_Employee"] = df["Revenue"] / df["Number_of_Employees"]
    df["Revenue_per_Customer"] = df["Revenue"] / df["Customers"]
    return df

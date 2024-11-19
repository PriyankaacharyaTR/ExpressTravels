import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.tripadvisor.com/Attractions-g187147-Activities-c42-Paris_Ile_de_France.html?page="

# Define the headers (to mimic a real user request)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
}

session = requests.Session()
session.headers.update(headers)

def extract_tourist_places(page_number):
    url = BASE_URL + str(page_number)
    print(f"Scraping page: {url}")
    
    response = session.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
        return []

    # Print the first 500 characters of the response to check if we are getting the expected content
    print(response.text[:500])  # To inspect if we're actually getting the page content

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Try to find the right elements for tourist places (you should inspect the structure manually if needed)
    attraction_elements = soup.find_all("div", class_="listing_title")
    
    if not attraction_elements:
        print(f"No attractions found on page {page_number}. Check the selectors.")
    
    tourist_places = []
    for element in attraction_elements:
        name = element.get_text(strip=True)
        link = "https://www.tripadvisor.com" + element.find('a')['href']
        
        # Visit the link to get more details (optional)
        details_response = session.get(link)
        details_soup = BeautifulSoup(details_response.text, "html.parser")

        description = details_soup.find("div", class_="attraction-detail-description").get_text(strip=True) if details_soup.find("div", class_="attraction-detail-description") else "No description available"
        location = details_soup.find("span", class_="address").get_text(strip=True) if details_soup.find("span", class_="address") else "No location"
        rating = details_soup.find("span", class_="overallRating").get_text(strip=True) if details_soup.find("span", class_="overallRating") else "No rating"
        images = [img['src'] for img in details_soup.find_all("img", class_="photo_image")][:3]  # Get up to 3 images

        tourist_places.append({
            "name": name,
            "location": location,
            "description": description,
            "rating": rating,
            "images": images
        })
    
    return tourist_places

def scrape_multiple_pages(total_pages=5):
    all_tourist_places = []

    for page_number in range(1, total_pages + 1):
        places_on_page = extract_tourist_places(page_number)
        all_tourist_places.extend(places_on_page)

    with open("tourist_places.json", "w", encoding="utf-8") as json_file:
        json.dump(all_tourist_places, json_file, ensure_ascii=False, indent=4)
    
    print(f"Data from {total_pages} pages has been saved to tourist_places.json.")

scrape_multiple_pages(total_pages=5)

----------------
 <div class="container">
        <%- include("../includes/flash.ejs") %><%-body%>
    </div>

--------------------------

const dbUrl = process.env.ATLASDB_URL;
const MongoStore = require('connect-mongo');
const passport=require("passport");
const LocalStrategy=require("passport-local");
const User=require("./models/user");
const store = MongoStore.create({
  mongoUrl: dbUrl,
  crypto: {
      secret: process.env.SECRET,
  },
  touchAfter: 24 * 3600,
});

store.on("error", () => {
  console.log("ERROR in MONGO SESSION STORE", err);
})

const sessionOption = {
  store:store,
  secret: process.env.SECRET,
  resave: false,
  saveUninitialized: true,
  cookie: {
      expires: Date.now() + 7 * 24 * 60 * 60 * 1000,
      maxAge: 7 * 24 * 60 * 60 * 1000,
      httpOnly:true,
  },
};
app.use(session(sessionOption));

app.use(passport.initialize());
app.use(passport.session());
passport.use(new LocalStrategy(User.authenticate()));

passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

app.get("/demouser", async (req, res) => {
    let fakeUser = new User({
        email: "student@gmail.com",
        username: "delta-student"
    });

    let registeredUser = await User.register(fakeUser, "helloworld");
    res.send(registeredUser);
});

------------------
async function callGeminiAPI(place){
    const { GoogleGenerativeAI } = require("@google/generative-ai");

    const genAI = new GoogleGenerativeAI("AIzaSyDNlcDPG9J6wAAukxFklXYRoFDLFObedfg");
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });
    
    const prompt =  `Tell me about the local cuisine, tourist attractions, hidden gems, and handicrafts/products famous around ${place}.`;
    
    try{
      const result = await model.generateContent(prompt);
      console.log(result.response.text());
      const data = await response.json();
        console.log('Gemini API Response:', data);

        showToast(data.choices[0].text);
    }
    catch (error) {
      if (error.response && error.response.status === 503 && retryCount < MAX_RETRIES) {
          console.log(`Retrying... Attempt ${retryCount + 1}`);
          retryCount++;
          setTimeout(fetchGeminiData, 5000);  // Retry after 5 seconds
      } else {
          console.error('Error fetching data from Gemini API:', error);
      }
  }


}
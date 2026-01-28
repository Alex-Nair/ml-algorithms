from playwright.sync_api import sync_playwright

leftovers = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless = False)
    page = browser.new_page()
    

    def readRecipes():
        links = page.locator("a.promo").evaluate_all("elements => elements.map(element => element.href)")
        links = [link for link in links if "recipes" in link]

        for link in links:
            page.goto(link)
            
            header = ""
            description = ""
            ingredients = ""
            steps = ""

            headerElement = page.locator("#main-heading")
            if headerElement.count() > 0:
                header = headerElement.inner_html()

            descriptionElement = page.locator("p.ssrcss-19e4ohh-StyledHtmlParser")
            if descriptionElement.count() > 0:
                description = page.locator("p.ssrcss-19e4ohh-StyledHtmlParser").inner_html()

            ingredientsElement = page.locator("ul.ssrcss-1ynsflq-UnorderedList")
            if ingredientsElement.count() > 0:
                ingredients = ""
                for ingredientList in ingredientsElement.all():
                    for element in ingredientList.locator("li.ssrcss-ugdhan-Stack").all():
                        ingredients += element.text_content() + "|"
                
                ingredients = ingredients[:-1] # Get rid of the trailing |

            stepsElement = page.locator("ol.ssrcss-1o787j8-OrderedList")
            if stepsElement.count() > 0:
                steps = ""
                for stepList in stepsElement.all():
                    for element in stepList.locator("li.ssrcss-ugdhan-Stack").all():
                        steps += element.text_content() + "|"
                
                steps = steps[:-1] # Get rid of the trailing |

            recipe = {
                "name": header,
                "description": description,
                "ingredients": ingredients,
                "steps": steps
            }
            
            # A list of strings that should be replaced in order to comply with basic ASCII encoding.
            replacementStrings = {
                "½": ".5",
                "¼": ".25",
                "¾": ".75",
                "–": "-"
            }

            for tag in recipe.keys(): # Dataset cleaning - Replace common fractions with decimals.
                for replacementString in replacementStrings.keys():
                    recipe[tag] = recipe[tag].replace(replacementString, replacementStrings[replacementString])

            try:
                with open("data.txt", "a") as file:
                    stringToAdd = ""
                    for tag in recipe.keys():
                        stringToAdd += recipe[tag] + "\n"
                    
                    file.write(stringToAdd)
            
            except Exception as e:
                leftovers.append(recipe) # Error encountered with this recipe. Save it to a new list we can output at the end.
    
    #["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r" "s", "w", "x", "y", "z", "0-9"]
    for header in ["m", "n", "o", "p", "q", "r" "s", "w", "x", "y", "z", "0-9"]:
        pageNumber = 1
        isStillValid = True

        while isStillValid:
            page.goto(f"https://www.bbc.co.uk/food/recipes/a-z/{header}/{pageNumber}#featured-content")

            if not "Recipes | " in page.title():
                isStillValid = False
            
            else:
                readRecipes()
                pageNumber += 1

    browser.close()

print(leftovers) # Leftovers that caused errors.
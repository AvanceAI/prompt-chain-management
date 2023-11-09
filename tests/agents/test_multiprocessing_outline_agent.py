import pytest
from src.step_execution.variable_store import VariableStore
from src.agents.multiprocessing_outline_agent import MultiprocessingOutlineAgent 

@pytest.fixture
def agent_params():
    return {
        "dependencies": ["search_results", "themes", "selected_theme_key"],
                "query_params": {
          "model": "gpt-4",
          "temperature": 0,
          "max_tokens": 2000,
          "top_p": 0,
          "frequency_penalty": 0,
          "presence_penalty": 0,
          "eval_literal": True
        },
        "prompt_text": "Create an outline of the article below that includes the title and every section. Under each section, produce a detailed bullet point list that contains a concise summary of every piece of important or relevant information in the article. Don't miss the small but important details.\n\nAs you create the bullet point lists, state the information as succinctly as possible with as few words as possible. Paraphrase the information so that it contains the same meaning but does not use the same words of the original article. Include all relevant numbers, time lines, and dates.\n- Example: Requirements for K-1 applicants include proving that the marriage is bonafide and that they entered in marriage in good faith.  The marriage must be at least 2 years old. Applicants must be able to prove bonafide and good faith requirements within 10 days of interview and before October 2022. --> K-1 applicants must prove marriage > 2 years old and entered in good faith. Marriage must be bonafide. Must prove bonafide and good faith within 10 days of interview and before October 2022.\n\nArticle:\n\n{{article}}\n\n\n// end of article\n\nPrompt Reminder:\nAs you create the bullet point lists, state the information as succinctly as possible with as few words as possible. Paraphrase the information so that it contains the same meaning but does not use the same words of the original article. Include all relevant numbers, time lines, and dates.\n- Example: Requirements for K-1 applicants include proving that the marriage is bonafide and that they entered in marriage in good faith.  The marriage must be at least 2 years old. Applicants must be able to prove bonafide and good faith requirements within 10 days of interview and before October 2022. --> K-1 applicants must prove marriage > 2 years old and entered in good faith. Marriage must be bonafide. Must prove bonafide and good faith within 10 days of interview and before October 2022.\n",
    }

@pytest.fixture
def variable_store(themes, search_results):
    return VariableStore(save_dir="tests", variables={"search_results": search_results, "themes": themes, "selected_theme_key": '0'})

@pytest.mark.asyncio
async def test_execute(agent_params, variable_store):
    agent = MultiprocessingOutlineAgent(agent_params)
    result = await agent.execute(variable_store)
    assert isinstance(result, dict)

@pytest.fixture
def search_results():
    return {
        "0": {
            "title": "voidtools",
            "description": "Everything. Locate files and folders by name instantly. Everything. Small installation file. Clean and simple user interface. Quick filename indexing. Quick ...",
            "href": "https://www.voidtools.com/"
        },
        "1": {
            "title": "Sous Vide Everything - YouTube",
            "description": "Sous Vide Everything is all about amazing food! The channel is dedicated to the search of perfectly cooked proteins and more. The name says it all!",
            "href": "https://www.youtube.com/@SousVideEverything"
        },
        "2": {
            "title": "Everything Downloads",
            "description": "Download Everything 1.4.1.1024. Download Installer Download Installer 64-bit ... All Everything Downloads. Everything-1.4.1.1024.x86-Setup.exe. Installer, x86 ...",
            "href": "https://www.voidtools.com/downloads/"
        },
        "3": {
            "title": "Everything Definition & Meaning - Merriam-Webster",
            "description": "The meaning of EVERYTHING is all that exists. How to use everything in a sentence.",
            "href": "https://www.merriam-webster.com/dictionary/everything"
        },
        "4": {
            "title": "Everything on Steam",
            "description": "Apr 21, 2017 ... Everything is an interactive experience where every object in the Universe is a playable character - from animals to planets to galaxies and ...",
            "href": "https://store.steampowered.com/app/582270/Everything/"
        },
        "5": {
            "title": "Explain Everything | Interactive Whiteboard for Teaching",
            "description": "Explain Everything is your all-in-one tool for engaging lessons ... Explain any concept 1:1 or during group sessions. Use voice chat and collaborative editing to ...",
            "href": "https://explaineverything.com/"
        },
        "6": {
            "title": "EVERYTHING Definition & Usage Examples | Dictionary.com",
            "description": "everything · every single thing or every particular of an aggregate or total; all. · something extremely important: This news means everything to us.",
            "href": "https://www.dictionary.com/browse/everything"
        },
        "7": {
            "title": "The Band Everything – thebandeverything",
            "description": "We are returning to Hampton, VA! Sept. 24 at Vanguard Brewpub ... Ok Friends - As we continue on our new journey as THE BAND EVERYTHING, we are trying to ...",
            "href": "https://thebandeverything.com/"
        },
        "8": {
            "title": "Jamie Milne (@everything_delish) • Instagram photos and videos",
            "description": "a little bit of everything | self-taught cook & eater ✨tiktok: @everything_delish (2.6M+) ✨pinterest: everythingdelish (250K+). NEW RECIPE ⬇️.",
            "href": "https://www.instagram.com/everything_delish/?hl=en"
        },
        "9": {
            "title": "Everything, Everything (2017) - IMDb",
            "description": "Everything, Everything: Directed by Stella Meghie. With Amandla Stenberg, Nick Robinson, Anika Noni Rose, Ana de la Reguera. A teenager who's spent her ...",
            "href": "https://www.imdb.com/title/tt5001718/"
        },
        "10": {
            "title": "Discussion Guide for Everything Happens for a Reason (And Other ...",
            "description": "An instant New York Times bestseller, Everything Happens for a Reason tells her story, offering up her irreverent, hard-won observations on dying and the ways ...",
            "href": "https://katebowler.com/download/everything-happens-discussion-questions/"
        },
        "11": {
            "title": "Watch Everything Now | Netflix Official Site",
            "description": "Sep 6, 2023 ... After months in recovery for an eating disorder, 16-year-old Mia devises a bucket list of quintessential teen experiences to make up for ...",
            "href": "https://www.netflix.com/title/81437049"
        },
        "12": {
            "title": "Everything - Wikipedia",
            "description": "Without expressed or implied limits, it may refer to anything. The universe is everything that exists theoretically, though a multiverse may exist according to ...",
            "href": "https://en.wikipedia.org/wiki/Everything"
        },
        "13": {
            "title": "Everything Christmas",
            "description": "Find video, photos and more for the Hallmark Channel Christmas movie “Everything Christmas,” starring Katherine Barrell, Cindy Busby, Corey Sevier and Matt ...",
            "href": "https://www.hallmarkchannel.com/everything-christmas"
        },
        "14": {
            "title": "Everything Cheesy Potato and Egg Breakfast Casserole. - Half ...",
            "description": "Dec 26, 2018 ... Ingredients · ▢ 3 cups leftover mashed potatoes · ▢ 3/4 cup whole milk · ▢ 1 cup shredded sharp cheddar cheese · ▢ 1/2 cup shredded Havarti ...",
            "href": "https://www.halfbakedharvest.com/everything-cheesy-potato-and-egg-breakfast-casserole/"
        },
        "15": {
            "title": "Everything Notebook – Raul Pacheco-Vega, PhD",
            "description": "Feb 2, 2017 ... This post explains what I use the Everything Notebook for: planning and scheduling my weekly, and daily To-Do lists, as well as maintaining my ...",
            "href": "http://www.raulpacheco.org/resources/the-everything-notebook/"
        },
        "16": {
            "title": "Everything Bar - Gourmet Chocolate Bar by Compartes Los Angeles",
            "description": "The Everything Bar by Compartes Los Angeles. A gourmet chocolate bar with brownies, pretzels, potato chip chocolate, sprinkles, marshmallows, cake and a mix ...",
            "href": "https://compartes.com/products/everything-bar-gourmet-chocolate-bar"
        },
        "17": {
            "title": "Select all variables or the last variable — everything • tidyselect",
            "description": "These functions are selection helpers. everything() selects all variable. It is also useful in combination with other tidyselect operators. last_col() ...",
            "href": "https://tidyselect.r-lib.org/reference/everything.html"
        },
        "18": {
            "title": "Everything Everything",
            "description": "Everything Everything. Home · Live · Music · Store · EEE Pass Sign up to newsletter. [01]. Everything Everything - New Album ...",
            "href": "https://everything-everything.co.uk/"
        },
        "19": {
            "title": "Everything Is Broken. Once upon a time, a friend of mine… | by ...",
            "description": "May 20, 2014 ... Everything Is Broken ... Once upon a time, a friend of mine accidentally took over thousands of computers. He had found a vulnerability in a piece ...",
            "href": "https://medium.com/message/everything-is-broken-81e5f33a24e1"
        }
    }
    
@pytest.fixture
def themes():
    return {'0': {'theme': 'Software/Technology', 'results': [0, 2]}, '1': {'theme': 'Food/Cooking', 'results': [1, 14, 16]}, '2': {'theme': 'Definition/Explanation', 'results': [3, 6]}, '3': {'theme': 'Entertainment', 'results': [4, 11, 19]}, '4': {'theme': 'Education/Teaching', 'results': [5, 15]}, '5': {'theme': 'Music', 'results': [7, 18]}, '6': {'theme': 'Social Media/Influencers', 'results': [8]}, '7': {'theme': 'Film/TV', 'results': [9]}, '8': {'theme': 'Books/Literature', 'results': [10]}, '9': {'theme': 'Christmas/Holidays', 'results': [12, 13]}, '10': {'theme': 'Productivity/Planning', 'results': [15]}, '11': {'theme': 'Chocolate/Desserts', 'results': [16]}, '12': {'theme': 'Data Analysis/Selection', 'results': [17]}, '13': {'theme': 'Music', 'results': [18]}, '14': {'theme': 'Technology/Internet', 'results': [19]}}
import pytest
from src.step_execution.variable_store import VariableStore
from src.agents.llm_query_agent import LlmQueryAgent

@pytest.fixture
def agent_params():
    return {
        "dependencies": ["topic", "search_results"],
                "query_params": {
          "model": "gpt-3.5-turbo-instruct",
          "temperature": 0,
          "max_tokens": 1000,
          "top_p": 1,
          "frequency_penalty": 0,
          "presence_penalty": 0,
          "eval_literal": True
        },
        "prompt_text": "I have a list of search results related to the topic \"{topic}\". Please analyze the following data and group the results into 3-4 thematic categories based on their content and purpose. You may ignore uncommon themes and focus on the most prominent categories presented in these results. Here is the data:\n\n\n{search_results}\n\n\nBased on the titles and descriptions, please provide a brief overview of each identified category and list which entries (by their number) belong to each category.\n\nFormat your response like this.\n\nResponse:\n{{\n\"0\": {{\n       \"theme\": \"First theme identified\",\n       \"results\": [0, 4, 5, 7, 9] \n       }},\n\"1\": {{\n       \"theme\": \"First theme identified\",\n       \"results\": [1,8,11,13] \n       }},\n\"2\": {{\n       \"theme\": \"First theme identified\",\n       \"results\": [2,3, 6] \n       }}\n}}\n\n\nResponse:\n",
    }

@pytest.fixture
def variable_store(search_results):
    return VariableStore(save_dir="tests", variables={"topic": "Everything", "search_results": search_results})

@pytest.mark.asyncio
async def test_execute(agent_params, variable_store):
    agent = LlmQueryAgent(agent_params)
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
import pytest
import asyncio
from unittest.mock import AsyncMock
from src.services.chain_service.step_execution.step_executor import StepExecutor
from src.models.chain import Step
from src.repository.prompt_db.json_repository import JsonRepository
from src.services.chain_service.dependency_resolver import DependencyResolver

def mock_repository(tmp_path):
    repository_file = tmp_path / "test_step_chain.json"
    repository_file.write_text('{}')  # Initialize the file with an empty JSON object
    return JsonRepository(filename=str(repository_file))

@pytest.fixture
def dependency_resolver():
    send_callback = AsyncMock()
    return DependencyResolver(send_callback=send_callback)

@pytest.mark.asyncio
async def test_execute_search_step(dependency_resolver):
    step_executor = StepExecutor(run_id="test_run", save_dir="outputs", dependency_resolver=dependency_resolver)

    step_dict = {
        "step_id": "search-for-topic",
        "description": "Uses Google Search API to perform a search on a topic and return the top results in JSON form.",
        "agent": "search",
        "response_type": "json",
        "dependencies": [
          {
            "name": "topic",
            "type": "str",
            "class": "user_entry",
            "message": "What topic would you like to write about?"
          }
      ],
        "outputs": [
          {
            "name": "search_results",
            "type": "json",
            "class": "output"
          }
        ],
        "actions": None
      }
    
    step = Step(**step_dict)
    
    # Arrange: Set the correlation id and simulate the user input
    correlation_id = f"{step.step_id}-topic"
    user_input = "Artificial Intelligence"
    
    # Act: Create a task to execute the step which would internally await user input
    execute_task = asyncio.create_task(step_executor.execute_step(step))

    # Wait a bit for request_user_input to be called
    await asyncio.sleep(0.01) 

    # Simulate user input by calling resolve_user_input directly
    dependency_resolver.resolve_user_input(correlation_id, user_input)

    # Now await the step execution to complete
    search_results = await execute_task

    # Assert: Ensure that the search_results contain 20 keys as expected
    assert len(list(search_results.keys())) == 20
    # Additional assert can be done to check if the mock send_callback was called with the right parameters
    dependency_resolver.send_callback.assert_called_once_with({
        "type": "user_entry",
        "correlation_id": correlation_id,
        "message": step_dict['dependencies'][0]['message'],
        "variable": None
    })

@pytest.mark.asyncio
async def test_execute_llm_query_step():
    def mock_send_callback(dep_key): # No user input variables for this step
        data = {}
        return data[dep_key]
   
    mock_variables = {
          "topic": "DS-260 Form",
          "search_results": {
        "0": {
            "title": "DS-260 Immigrant Visa Electronic Application - Frequently Asked ...",
            "description": "Travel.State.Gov > U.S. Visas > Forms > Online Immigrant Visa Forms > DS-260 Immigrant Visa Electronic Application - Frequently Asked Questions (FAQs) ...",
            "href": "https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/forms/online-immigrant-visa-forms/ds-260-faqs.html"
        },
        "1": {
            "title": "Consular Electronic Application Center",
            "description": "DS-261, Online Choice of Address and Agent · Fee Payment · DS-260, Online Immigrant Visa and Alien Registration Application · Check My Visa Application Status.",
            "href": "https://ceac.state.gov/"
        },
        "2": {
            "title": "Online Application",
            "description": "Step 6: Complete Online Visa Application (DS-260) ... After you pay your fees and the status in CEAC is updated to 'PAID', you and each qualified family member ...",
            "href": "https://travel.state.gov/content/travel/en/us-visas/immigrate/the-immigrant-visa-process/step-5-collect-financial-evidence-and-other-supporting-documents/step-6-complete-online-visa-application.html"
        },
        "3": {
            "title": "Department of State (DS) and Other Non-USCIS Forms | USCIS",
            "description": "Jan 11, 2018 ... DS-260: Online Immigrant Visa Application · DS-160: Online Nonimmigrant Visa Application · DS-230: Application for Immigrant Visa and Alien ...",
            "href": "https://www.uscis.gov/forms/department-of-state-ds-and-other-non-uscis-forms"
        },
        "4": {
            "title": "Submit Your Immigrant Visa and Alien Registration Application",
            "description": "The principal applicant and all family members applying for a diversity visa program must complete Form DS-260. You will need to enter your DV case number ...",
            "href": "https://travel.state.gov/content/travel/en/us-visas/immigrate/diversity-visa-program-entry/diversity-visa-if-you-are-selected/diversity-visa-submit-your-iv-and-alien-registration-application.html"
        },
        "5": {
            "title": "Complete your Form DS-260 as it is in your Passport - U.S. Embassy ...",
            "description": "May 8, 2023 ... Complete your Form DS-260 as it is in your Passport · When filling out your DS-260 form for an immigrant visa, the information you enter on the ...",
            "href": "https://do.usembassy.gov/complete-your-form-ds-260-as-it-is-in-your-passport-2/"
        },
        "6": {
            "title": "DS-260 Information - U.S. Embassy & Consulates in Russia",
            "description": "Each applicant – including children – must have their own DS-260 visa application. The DS-260 form must be submitted online and the printed confirmation ...",
            "href": "https://ru.usembassy.gov/visas/immigrant-visas/iv-ds260-faq/"
        },
        "7": {
            "title": "Complete your Form DS-260 as it is in your Passport - U.S. Embassy ...",
            "description": "Sep 19, 2022 ... Complete your Form DS-260 as it is in your Passport ... When filling out your DS-260 form for an immigrant visa, the information must appear as in ...",
            "href": "https://do.usembassy.gov/complete-your-form-ds-260-as-it-is-in-your-passport/"
        },
        "8": {
            "title": "DS-260 Form and Instructions - Consular Electronic Application ...",
            "description": "The DS-261 application is relatively simple. Essentially, the DS-261 form gives the State Department details on how to reach you. Form DS-261 must be processed ...",
            "href": "https://lawfirm1.com/immigration-forms/ds-260-form/"
        },
        "9": {
            "title": "Visas: Documentation of Immigrants Under the ... - Federal Register",
            "description": "Aug 3, 2010 ... (a) Application Forms. (1) Application on Form DS–230 or Form DS–260 Required. —Every alien applying for an immigrant visa must make ...",
            "href": "https://www.federalregister.gov/documents/2010/08/03/2010-19046/visas-documentation-of-immigrants-under-the-immigration-and-nationality-act-as-amended"
        },
        "10": {
            "title": "LIST OF DOCUMENTS WHICH DV LOTTERY WINNERS MUST ...",
            "description": "Complete form DS-260 Online Immigrant Visa Application. To access DS-260, you will need to enter your DV visa case number. A separate form is required for each ...",
            "href": "https://lv.usembassy.gov/wp-content/uploads/sites/58/List-of-Documents-which-DV-Lottery-Winners-Must-Prepare.pdf"
        },
        "11": {
            "title": "DS-260 Immigrant Visa and Alien Registration Application",
            "description": "Application. This form is completed online. Further instructions are available on the travel.state.gov site at:.",
            "href": "https://eforms.state.gov/Forms/ds260.PDF"
        },
        "12": {
            "title": "Dear Adoptive Parents and Adoption Service Providers: On ...",
            "description": "... DS-260 form with your specific case number. You can email this information ... DS-260 form for your adopted child/children: 1. Please go to https://ceac ...",
            "href": "https://ua.usembassy.gov/wp-content/uploads/sites/151/2017/04/DS-260-for-Webpage_Adoptions-with-corrections.pdf"
        },
        "13": {
            "title": "DS-260 Form - Step-By-Step Complete Guide",
            "description": "DS-260 Checklist · Copy of your current passport; · Birth certificate (with English translation if necessary); · Police clearance certificate if over the age of ...",
            "href": "https://self-lawyer.com/ds-260-form-step-by-step-complete/"
        },
        "14": {
            "title": "Checklist for Your Family-Based Visa Interview - U.S. Embassy in ...",
            "description": "VISA APPLICATION. Complete the visa application (Form DS-260) online for each immigrant visa applicant at https://ceac.state.gov/IV/Login.aspx and print the ...",
            "href": "https://il.usembassy.gov/visas/immigrant-visas/family-based-immigration/checklist/"
        },
        "15": {
            "title": "9 FAM 504.5 (U) PRE-INTERVIEW PROCESSING",
            "description": "If Form DS-260 is incomplete, the document checker must reopen the application via the “Reopen DS-260” button at the top of the online IV application report and ...",
            "href": "https://fam.state.gov/fam/09FAM/09FAM050405.html"
        },
        "16": {
            "title": "Online Immigrant Visa and Alien Registration Application (DS-260 ...",
            "description": "a severe form of trafficking in persons? Yes No. • Are you the spouse, son, or daughter of an individual who has committed or conspired to commit a human ...",
            "href": "https://www.shusterman.com/pdf/DS-260.pdf"
        },
        "17": {
            "title": "Social Security Numbers and Immigrant Visas",
            "description": "Collect information needed for a Social Security number on Form DS-230 (Application for Immigrant Visa and Alien Registration) or Form DS-260 (Immigrant ...",
            "href": "https://www.ssa.gov/ssnvisa/whatyou_need.htm"
        },
        "18": {
            "title": "INSTRUCTIONS FOR IMMIGRANT VISA APPLICANTS",
            "description": "Jan 1, 2019 ... STEP 1: For each family member who is eligible to travel to the United States, fill out the DS-. 260 Form ... DS-260 login page. Important Note ...",
            "href": "https://it.usembassy.gov/wp-content/uploads/sites/67/INSTRUCTIONS_FOR_IMMIGRANT.pdf"
        },
        "19": {
            "title": "What is Enumeration at Entry and how does it work?",
            "description": "Jan 26, 2023 ... ... (Form DS-230 or DS-260) at a Department of State ... We will mail your SSN card to the address you listed on your DS-230 or DS-260 application.",
            "href": "https://faq.ssa.gov/en-us/Topic/article/KA-10040"
        }
    }
          }
    
    mock_resolver = DependencyResolver(send_callback=mock_send_callback)
    step_executor = StepExecutor(run_id="test_run", save_dir="outputs", dependency_resolver=mock_resolver, variables=mock_variables)

    step_dict = {
        "step_id": "find-themes",
        "description": "Analyzes the search results and finds the most common themes, which are then presented to the user to refine the article topic.",
        "agent": "llm-query",
        "query_params": {
            "model": "gpt-4",
            "temperature": 0,
            "max_tokens": 1000,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
          },
        "prompt_text": "I have a list of search results related to the topic \"{topic}\". Please analyze the following data and group the results into 3-4 thematic categories based on their content and purpose. You may ignore uncommon themes and focus on the most prominent categories presented in these results. Here is the data:\n\n\n{search_results}\n\n\nBased on the titles and descriptions, please provide a brief overview of each identified category and list which entries (by their number) belong to each category.\n\nFormat your response like this.\n\nResponse:\n{{\n\"0\": {{\n       \"theme\": \"First theme identified\",\n       \"results\": [0, 4, 5, 7, 9] \n       }},\n\"1\": {{\n       \"theme\": \"First theme identified\",\n       \"results\": [1,8,11,13] \n       }},\n\"2\": {{\n       \"theme\": \"First theme identified\",\n       \"results\": [2,3, 6] \n       }}\n}}\n\n\nResponse:\n",
        "response_type": "json",
        "dependencies": [
          {
            "name": "topic",
            "type": "str",
            "class": "input"
          },
          {
            "name": "search_results",
            "type": "json",
            "class": "input"
          }
        ],
        "outputs": [
          {
            "name": "themes",
            "type": "json",
            "class": "output"
          }
        ],
        "actions": [
          {
            "name": "select-preferred-theme",
            "type": "select",
            "data": "themes"
          }
        ]
      }
    

    # Test GPT-3.5-Turbo-Instruct
    step_dict["query_params"]["model"] = "gpt-3.5-turbo-instruct"
    step = Step(**step_dict)
    themes = await step_executor.execute_step(step)
    assert isinstance(themes, dict)
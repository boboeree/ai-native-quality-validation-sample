import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="23704433-c18a-4572-a704-27a494adf986",
    name="Verify Budget Property Listings",
    tc_id="TC-7",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"budget_properties_heading": "Budget properties", "budget_properties_summary": "2 total properties", "brooklyn_new_york_property_card": "Brooklyn, New York at $120 per night", "scottsdale_arizona_property_card": "Scottsdale, Arizona at $145 per night", "excluded_listing_prices": "true", "property_card_nightly_price_limit": "true"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/', instruction_id='7475923e-a938-4579-bbea-7a189e8b83fb'):
        await page.goto("https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/")
    
    async with testmu.step('Clicking Budget category filter 🎯', instruction_id='dbfebcc9-52f1-43c4-a864-a9c06cf39448'):
        _loc_1 = page.locator("internal:role=button[name=\"🎯 Budget\"i]")
        
        await _loc_1.click()
    
    async with testmu.step('Waiting 1 second for Budget listing results to settle', instruction_id='29a3dc27-c6f1-484d-b4c4-08b07b0ff644'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Reading the budget property section heading'):
        set_var('budget_properties_heading', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {29: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(29).innerText);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:role=heading[name="Budget properties"i]'], query='the budget property section heading', expected_value='Budget properties', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The heading is "Budget properties".'))
    
    async with testmu.step('Reading the budget property summary'):
        set_var('budget_properties_summary', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {30: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(30).innerText);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="total properties"i'], query='the total-property summary in the budget section', expected_value='2 total properties', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='The summary is exactly "2 total properties".'))
    
    async with testmu.step('Reading the Brooklyn property card location and nightly price'):
        set_var('brooklyn_new_york_property_card', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {31: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((()=>{const t=el(31).innerText;const n=el(31).querySelector('h3').innerText;const p=t.match(/\\$(\\d+)\\s*night/);return p?`${n} at $${p[1]} per night`:null})());\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="←→Brooklyn, New York4."i'], query='the location and nightly price of the Brooklyn property card', expected_value='Brooklyn, New York at $120 per night', needs_unit_conversion=False, operator='equals', transforms=[], condition='The only two property cards include Brooklyn, New York at $120 per night.'))
    
    async with testmu.step('Reading the Scottsdale property card location and nightly price'):
        set_var('scottsdale_arizona_property_card', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {44: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((()=>{const t=el(44).innerText;const n=el(44).querySelector('h3').innerText;const p=t.match(/\\$(\\d+)\\s*night/);return p?`${n} at $${p[1]} per night`:null})());\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="←→Scottsdale, Arizona4.4Condo"i'], query='the location and nightly price of the Scottsdale property card', expected_value='Scottsdale, Arizona at $145 per night', needs_unit_conversion=False, operator='equals', transforms=[], condition='The only two property cards include Scottsdale, Arizona at $145 per night.'))
    
    async with testmu.step('Checking the visible listing prices'):
        set_var('excluded_listing_prices', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {31: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((()=>{const t=el(31).innerText;return !/\\$(165|275|280)(?:\\s|$)/.test(t)})());\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="←→Brooklyn, New York4."i'], query='whether the visible listing prices exclude 165, 275, and 280 dollars', expected_value='true', needs_unit_conversion=False, operator='equals', transforms=[], condition='$165, $275, and $280 do not appear as listing prices.'))
    
    async with testmu.step('Checking the visible property-card nightly prices'):
        set_var('property_card_nightly_price_limit', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {31: 0, 44: 1};\n  const el = (i) => els[__m[i]];\n  const __v = ((()=>{const cards=[el(31),el(44)];const prices=cards.map(c=>{const m=c.innerText.match(/\\$(\\d+)\\s*night/);return m?Number(m[1]):NaN});return prices.length===2&&prices.every(p=>p<=150)})());\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="←→Brooklyn, New York4."i', 'internal:text="←→Scottsdale, Arizona4.4Condo"i'], query='whether the two visible property cards have nightly prices at or below 150 dollars', expected_value='true', needs_unit_conversion=False, operator='equals', transforms=[], condition='No visible property-card nightly price exceeds $150.'))
    
    async with testmu.step('Assertion check', instruction_id='de55fc99-8369-47d3-86ff-87fa5f2806e9'):
        await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'The heading is "Budget properties".', 'passed': True, 'operator': 'equals', 'transforms': ['strip'], 'json_path': None, 'expected': 'Budget properties', 'extracted_value': '{{budget_properties_heading}}', 'store_key': 'budget_properties_heading', 'variable_refs': {'{{budget_properties_heading}}': 'Budget properties'}}, {'description': 'The summary is exactly "2 total properties".', 'passed': True, 'operator': 'equals', 'transforms': ['strip'], 'json_path': None, 'expected': '2 total properties', 'extracted_value': '{{budget_properties_summary}}', 'store_key': 'budget_properties_summary', 'variable_refs': {'{{budget_properties_summary}}': '2 total properties'}}], 'sub_checks': [{'description': 'The heading is "Budget properties".', 'store_key': 'budget_properties_heading', 'expected_value': 'Budget properties', 'extracted_value': '{{budget_properties_heading}}', 'operator': 'equals', 'transforms': ['strip']}, {'description': 'The summary is exactly "2 total properties".', 'store_key': 'budget_properties_summary', 'expected_value': '2 total properties', 'extracted_value': '{{budget_properties_summary}}', 'operator': 'equals', 'transforms': ['strip']}], 'composite_operator': 'and', 'claim': 'the heading is "Budget properties" and the summary is exactly "2 total properties"'})
    
    async with testmu.step('Assertion check', instruction_id='59c76a25-ffe4-4272-be12-7ea91c4e7334'):
        await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'The only two property cards include Brooklyn, New York at $120 per night.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'Brooklyn, New York at $120 per night', 'extracted_value': '{{brooklyn_new_york_property_card}}', 'store_key': 'brooklyn_new_york_property_card', 'variable_refs': {'{{brooklyn_new_york_property_card}}': 'Brooklyn, New York at $120 per night'}}, {'description': 'The only two property cards include Scottsdale, Arizona at $145 per night.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'Scottsdale, Arizona at $145 per night', 'extracted_value': '{{scottsdale_arizona_property_card}}', 'store_key': 'scottsdale_arizona_property_card', 'variable_refs': {'{{scottsdale_arizona_property_card}}': 'Scottsdale, Arizona at $145 per night'}}], 'sub_checks': [{'description': 'The only two property cards include Brooklyn, New York at $120 per night.', 'store_key': 'brooklyn_new_york_property_card', 'expected_value': 'Brooklyn, New York at $120 per night', 'extracted_value': '{{brooklyn_new_york_property_card}}', 'operator': 'equals', 'transforms': []}, {'description': 'The only two property cards include Scottsdale, Arizona at $145 per night.', 'store_key': 'scottsdale_arizona_property_card', 'expected_value': 'Scottsdale, Arizona at $145 per night', 'extracted_value': '{{scottsdale_arizona_property_card}}', 'operator': 'equals', 'transforms': []}], 'composite_operator': 'and', 'claim': 'the only two property cards are Brooklyn, New York at $120 per night and Scottsdale, Arizona at $145 per night'})
    
    async with testmu.step('Assertion check', instruction_id='8fd51513-a7a3-491c-8f0c-a49fd4e1ca04'):
        await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'No visible property-card nightly price exceeds $150.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'true', 'extracted_value': '{{property_card_nightly_price_limit}}', 'store_key': 'property_card_nightly_price_limit', 'variable_refs': {'{{property_card_nightly_price_limit}}': 'true'}}, {'description': '$165, $275, and $280 do not appear as listing prices.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'true', 'extracted_value': '{{excluded_listing_prices}}', 'store_key': 'excluded_listing_prices', 'variable_refs': {'{{excluded_listing_prices}}': 'true'}}], 'sub_checks': [{'description': 'No visible property-card nightly price exceeds $150.', 'store_key': 'property_card_nightly_price_limit', 'expected_value': 'true', 'extracted_value': '{{property_card_nightly_price_limit}}', 'operator': 'equals', 'transforms': []}, {'description': '$165, $275, and $280 do not appear as listing prices.', 'store_key': 'excluded_listing_prices', 'expected_value': 'true', 'extracted_value': '{{excluded_listing_prices}}', 'operator': 'equals', 'transforms': []}], 'composite_operator': 'and', 'claim': 'no visible property-card nightly price exceeds $150 (in particular $165, $275, and $280 must not appear as listing prices)'})


if __name__ == "__main__":
    testmu.run(test)
import os
import json
from pathlib import Path
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="57d812de-b29c-4104-baa6-370149eb5136",
    name="Verify Property Listings by Price Category",
    tc_id="TC-6",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"property_card_count_check": "2 total properties", "brooklyn_property_price_check": "true", "visible_nightly_prices_max_check": "true", "no_275_property_visible_check": "false", "no_280_property_visible_check": "false", "scottsdale_property_price_check": "$145 night", "result_count_greater_than_two": "46 total properties(Page 1 of 3)", "properties_above_150_appear_again": "true"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    await page.set_viewport_size({"width": 1920, "height": 1080})
    try:
        raw = await page.evaluate("_ => {}", 'lambdatest_action: {"action":"getTestDetails"}')
        data = json.loads(raw) if isinstance(raw, str) else raw
        safe = {k: data.get(k) for k in ("test_id", "session_id", "build_id", "status", "name", "browser", "platform") if isinstance(data, dict) and k in data}
        Path("../artifacts/python/cloud-session.json").write_text(json.dumps(safe, indent=2))
        print("CLOUD_SESSION_METADATA", json.dumps(safe), flush=True)
    except Exception as exc:
        print("CLOUD_SESSION_METADATA_UNAVAILABLE", type(exc).__name__, flush=True)
    print("CODEX_REPAIR viewport=1920x1080; boolean expected_value propagated; assertions unchanged", flush=True)
    try:
        async with testmu.step('Navigate to https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/', instruction_id='946ff848-6284-4064-8264-a1198de4ff14'):
            await page.goto("https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/")
        
        async with testmu.step('Clicking the Budget category filter button', instruction_id='ed74cf7c-9007-4b70-a7cc-c1dcf577c79f'):
            _loc_1 = page.locator("internal:role=button[name=\"🎯 Budget\"i]")
            
            await _loc_1.click()
        
        async with testmu.step('Reading the reported property count'):
            set_var('property_card_count_check', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {30: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(30).innerText);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="total properties"i'], query='the total property count reported beside the budget properties heading', expected_value='2', needs_unit_conversion=False, operator='equals', transforms=['extract_number'], condition='Exactly two property cards remain.'))
        
        async with testmu.step('Checking the Brooklyn property card nightly price'):
            set_var('brooklyn_property_price_check', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {31: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(31).innerText.includes('Brooklyn') && /\\$\\s*120\\b/.test(el(31).innerText) && /night/.test(el(31).innerText));\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="←→Brooklyn, New York4."i'], query='whether the Brooklyn property card displays a nightly price of $120', expected_value='true', needs_unit_conversion=False, operator='equals', transforms=[], condition='A Brooklyn property at $120 per night remains.'))
        
        async with testmu.step('whether every visible property-card nightly price is at most $150', instruction_id='ec4cd9f2-695d-45d2-ae92-171c95f7b74c'):
            await page.screenshot(path="../artifacts/python/vision-before-1.png", full_page=False)
            set_var('visible_nightly_prices_max_check', await testmu.vision_query(page, "whether every visible property-card nightly price is at most $150", "", expected_value="true"))
        
        async with testmu.step('whether a property priced at $275 per night is visible', instruction_id='b1c42067-6f8e-414a-92f2-7ab06910a9ff'):
            await page.screenshot(path="../artifacts/python/vision-before-2.png", full_page=False)
            set_var('no_275_property_visible_check', await testmu.vision_query(page, "whether a property priced at $275 per night is visible", "", expected_value="false"))
        
        async with testmu.step('whether a property priced at $280 per night is visible', instruction_id='87796630-4e98-42ff-9ff1-abd91f12c90e'):
            await page.screenshot(path="../artifacts/python/vision-before-3.png", full_page=False)
            set_var('no_280_property_visible_check', await testmu.vision_query(page, "whether a property priced at $280 per night is visible", "", expected_value="false"))
        
        async with testmu.step('Reading the Scottsdale property card nightly price'):
            set_var('scottsdale_property_price_check', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {56: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(56).innerText);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="$145 night"i'], query='the nightly price displayed in the Scottsdale property card', expected_value='145', needs_unit_conversion=False, operator='equals', transforms=['extract_number'], condition='A Scottsdale property at $145 per night remains.'))
        
        async with testmu.step('Assertion check', instruction_id='e0c3a5e7-7157-48e6-bd1f-be43d45e1f51'):
            await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'Exactly two property cards remain.', 'passed': True, 'operator': 'equals', 'transforms': ['extract_number'], 'json_path': None, 'expected': '2', 'extracted_value': '{{property_card_count_check}}', 'store_key': 'property_card_count_check', 'variable_refs': {'{{property_card_count_check}}': '2 total properties'}}, {'description': 'A Brooklyn property at $120 per night remains.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'true', 'extracted_value': '{{brooklyn_property_price_check}}', 'store_key': 'brooklyn_property_price_check', 'variable_refs': {'{{brooklyn_property_price_check}}': 'true'}}, {'description': 'A Scottsdale property at $145 per night remains.', 'passed': True, 'operator': 'equals', 'transforms': ['extract_number'], 'json_path': None, 'expected': '145', 'extracted_value': '{{scottsdale_property_price_check}}', 'store_key': 'scottsdale_property_price_check', 'variable_refs': {'{{scottsdale_property_price_check}}': '$145 night'}}], 'sub_checks': [{'description': 'Exactly two property cards remain.', 'store_key': 'property_card_count_check', 'expected_value': '2', 'extracted_value': '{{property_card_count_check}}', 'operator': 'equals', 'transforms': ['extract_number']}, {'description': 'A Brooklyn property at $120 per night remains.', 'store_key': 'brooklyn_property_price_check', 'expected_value': 'true', 'extracted_value': '{{brooklyn_property_price_check}}', 'operator': 'equals', 'transforms': []}, {'description': 'A Scottsdale property at $145 per night remains.', 'store_key': 'scottsdale_property_price_check', 'expected_value': '145', 'extracted_value': '{{scottsdale_property_price_check}}', 'operator': 'equals', 'transforms': ['extract_number']}], 'composite_operator': 'and', 'claim': 'exactly two property cards remain: a Brooklyn property at $120 per night and a Scottsdale property at $145 per night.'})
        
        async with testmu.step('Assertion check', instruction_id='e0094a78-c486-4639-ac1c-de8038c2bd48'):
            await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'Every visible nightly price is at most $150.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'true', 'extracted_value': '{{visible_nightly_prices_max_check}}', 'store_key': 'visible_nightly_prices_max_check', 'variable_refs': {'{{visible_nightly_prices_max_check}}': 'true'}}, {'description': 'No $275 property is visible.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'false', 'extracted_value': '{{no_275_property_visible_check}}', 'store_key': 'no_275_property_visible_check', 'variable_refs': {'{{no_275_property_visible_check}}': 'false'}}, {'description': 'No $280 property is visible.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'false', 'extracted_value': '{{no_280_property_visible_check}}', 'store_key': 'no_280_property_visible_check', 'variable_refs': {'{{no_280_property_visible_check}}': 'false'}}], 'sub_checks': [{'description': 'Every visible nightly price is at most $150.', 'store_key': 'visible_nightly_prices_max_check', 'expected_value': 'true', 'extracted_value': '{{visible_nightly_prices_max_check}}', 'operator': 'equals', 'transforms': []}, {'description': 'No $275 property is visible.', 'store_key': 'no_275_property_visible_check', 'expected_value': 'false', 'extracted_value': '{{no_275_property_visible_check}}', 'operator': 'equals', 'transforms': []}, {'description': 'No $280 property is visible.', 'store_key': 'no_280_property_visible_check', 'expected_value': 'false', 'extracted_value': '{{no_280_property_visible_check}}', 'operator': 'equals', 'transforms': []}], 'composite_operator': 'and', 'claim': 'every visible nightly price is at most $150 and no $275 or $280 property is visible.'})
        
        async with testmu.step('Clicking All category filter 🌍 All', instruction_id='3c519f38-c096-4b4d-aab3-af76f82051ae'):
            _loc_2 = page.locator("internal:role=button[name=\"🌍 All\"i]")
            
            await _loc_2.click()
        
        async with testmu.step('Reading the total property result count'):
            set_var('result_count_greater_than_two', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {30: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(30).textContent);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="total properties(Page 1 of 3)"i'], query='the total property result count shown above the listings', expected_value='2', needs_unit_conversion=False, operator='gt', transforms=['extract_number'], condition='The result count is greater than two.'))
        
        async with testmu.step('Checking for listings priced above $150 per night'):
            set_var('properties_above_150_appear_again', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {43: 0, 56: 1, 69: 2, 82: 3, 95: 4, 108: 5, 121: 6, 134: 7, 147: 8, 160: 9, 173: 10, 186: 11, 199: 12, 212: 13, 225: 14, 238: 15, 251: 16, 264: 17, 277: 18, 290: 19};\n  const el = (i) => els[__m[i]];\n  const __v = ([el(43),el(56),el(69),el(82),el(95),el(108),el(121),el(134),el(147),el(160),el(173),el(186),el(199),el(212),el(225),el(238),el(251),el(264),el(277),el(290)].filter(e=>Number((e.textContent.match(/\\d+/)||['0'])[0])>150).length>0);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:text="$850 night"i', 'internal:text="$320 night"i', 'internal:text="$275 night"i', 'internal:text="$625 night"i', 'internal:text="$1200 night"i', 'internal:text="$425 night"i', 'internal:text="$380 night"i', 'internal:text="$495 night"i', 'internal:text="$120 night"i', 'internal:text="$1500 night"i', 'internal:text="$180 night"i', 'internal:text="$195 night"i', 'internal:text="$340 night"i', 'internal:text="$890 night"i', 'internal:text="$280 night"i', 'internal:text="$395 night"i', 'internal:text="$145 night"i', 'internal:text="$750 night"i', 'internal:text="$285 night"i', 'internal:text="$580 night"i'], query='whether listings priced above $150 per night are present', expected_value='true', needs_unit_conversion=False, operator='equals', transforms=[], condition='Properties priced above $150 appear again.'))
        
        async with testmu.step('Assertion check', instruction_id='36eda849-47a0-4e47-aef2-7daba5117e04'):
            await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'The result count is greater than two.', 'passed': True, 'operator': 'gt', 'transforms': ['extract_number'], 'json_path': None, 'expected': '2', 'extracted_value': '{{result_count_greater_than_two}}', 'store_key': 'result_count_greater_than_two', 'variable_refs': {'{{result_count_greater_than_two}}': '46 total properties(Page 1 of 3)'}}, {'description': 'Properties priced above $150 appear again.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'true', 'extracted_value': '{{properties_above_150_appear_again}}', 'store_key': 'properties_above_150_appear_again', 'variable_refs': {'{{properties_above_150_appear_again}}': 'true'}}], 'sub_checks': [{'description': 'The result count is greater than two.', 'store_key': 'result_count_greater_than_two', 'expected_value': '2', 'extracted_value': '{{result_count_greater_than_two}}', 'operator': 'gt', 'transforms': ['extract_number']}, {'description': 'Properties priced above $150 appear again.', 'store_key': 'properties_above_150_appear_again', 'expected_value': 'true', 'extracted_value': '{{properties_above_150_appear_again}}', 'operator': 'equals', 'transforms': []}], 'composite_operator': 'and', 'claim': 'the result count is greater than two, and properties priced above $150 appear again'})
        await page.screenshot(path="../artifacts/python/completed.png", full_page=False)
    except BaseException:
        await page.screenshot(path="../artifacts/python/failure.png", full_page=False)
        raise


if __name__ == "__main__":
    testmu.run(test)
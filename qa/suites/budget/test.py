import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="e01c3bec-c861-11f1-aa84-66b57ffc3e39",
    name="Verify Loft in Austin Listing Visibility",
    tc_id="TC-5",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"loft_in_austin_visible": "false"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/', instruction_id='4ec2a228cebe4ed49baaf959658890cc'):
        await page.goto("https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/")
    
    async with testmu.step("whether the 'Loft in Austin' listing card is visible", instruction_id='c3df72b7b6024473a3c22f3925e540fb'):
        set_var('loft_in_austin_visible', await testmu.vision_query(page, "whether the 'Loft in Austin' listing card is visible", "", expected_value='true'))
    
    async with testmu.step("the 'Loft in Austin' listing card is visible", instruction_id='b41e66b40b9d4318a3c706fb4c2d8ccc'):
        await testmu.verify_assertion(page, "the 'Loft in Austin' listing card is visible", {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_checks': [{'description': "The 'Loft in Austin' listing card is visible.", 'store_key': 'loft_in_austin_visible', 'expected_value': 'true', 'operator': 'equals', 'transforms': [], 'extracted_value': '{{loft_in_austin_visible}}', 'variable_refs': {'{{loft_in_austin_visible}}': 'false'}, 'json_path': None}], 'composite_operator': 'and', 'verification': "The current page shows the listing card named 'Loft in Austin'.", 'claim': "the 'Loft in Austin' listing card is visible"})


if __name__ == "__main__":
    testmu.run(test)
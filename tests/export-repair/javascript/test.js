import testmu, { resolveVar, setVar } from '@testmuai/playwright-bindings';
import { expect } from '@playwright/test';

testmu.configure({
  "build": "57d812de-b29c-4104-baa6-370149eb5136",
  "name": "Verify Property Listings by Price Category",
  "tcId": "TC-6",
  "network": (process.env.NETWORK ?? "false").toLowerCase() === "true",
  "autoHealVersion": "AH2",
  "defaultActionTimeoutMs": 10000,
  "defaultNavigationTimeoutMs": 60000,
  "kaneRunV4": true
});

testmu.test("Verify Property Listings by Price Category", async (page) => {
  let element_0, element_1;
  await testmu.step("Navigate to https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/", { instructionId: "946ff848-6284-4064-8264-a1198de4ff14" }, async () => {
    await page.goto("https://boboeree.github.io/ai-native-quality-validation-sample/pr-1/");
  });
  
  await testmu.step("Clicking the Budget category filter button", { instructionId: "ed74cf7c-9007-4b70-a7cc-c1dcf577c79f" }, async () => {
    element_0 = page.locator("internal:role=button[name=\"\ud83c\udfaf Budget\"i]");
    await element_0.click();
  });
  
  await testmu.step("Reading the reported property count", async () => {
    await page.waitForLoadState("domcontentloaded", { timeout: 5000 });
    setVar("property_card_count_check", await testmu.textualAnalyzer(page, { wrappedJs: "(els) => {\n  const __m = {30: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(30).innerText);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators: ["internal:text=\"total properties\"i"], query: "the total property count reported beside the budget properties heading", expectedValue: "2", needsUnitConversion: false, operator: "equals", transforms: ["extract_number"], condition: "Exactly two property cards remain." }));
  });
  
  await testmu.step("Checking the Brooklyn property card nightly price", async () => {
    await page.waitForLoadState("domcontentloaded", { timeout: 5000 });
    setVar("brooklyn_property_price_check", await testmu.textualAnalyzer(page, { wrappedJs: "(els) => {\n  const __m = {31: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(31).innerText.includes('Brooklyn') && /\\$\\s*120\\b/.test(el(31).innerText) && /night/.test(el(31).innerText));\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators: ["internal:text=\"\u2190\u2192Brooklyn, New York4.\"i"], query: "whether the Brooklyn property card displays a nightly price of $120", expectedValue: "true", needsUnitConversion: false, operator: "equals", transforms: [], condition: "A Brooklyn property at $120 per night remains." }));
  });
  
  await testmu.step("whether every visible property-card nightly price is at most $150", { instructionId: "ec4cd9f2-695d-45d2-ae92-171c95f7b74c" }, async () => {
    setVar("visible_nightly_prices_max_check", await testmu.visionQuery(page, "whether every visible property-card nightly price is at most $150", ""));
  });
  
  await testmu.step("whether a property priced at $275 per night is visible", { instructionId: "b1c42067-6f8e-414a-92f2-7ab06910a9ff" }, async () => {
    setVar("no_275_property_visible_check", await testmu.visionQuery(page, "whether a property priced at $275 per night is visible", ""));
  });
  
  await testmu.step("whether a property priced at $280 per night is visible", { instructionId: "87796630-4e98-42ff-9ff1-abd91f12c90e" }, async () => {
    setVar("no_280_property_visible_check", await testmu.visionQuery(page, "whether a property priced at $280 per night is visible", ""));
  });
  
  await testmu.step("Reading the Scottsdale property card nightly price", async () => {
    await page.waitForLoadState("domcontentloaded", { timeout: 5000 });
    setVar("scottsdale_property_price_check", await testmu.textualAnalyzer(page, { wrappedJs: "(els) => {\n  const __m = {56: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(56).innerText);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators: ["internal:text=\"$145 night\"i"], query: "the nightly price displayed in the Scottsdale property card", expectedValue: "145", needsUnitConversion: false, operator: "equals", transforms: ["extract_number"], condition: "A Scottsdale property at $145 per night remains." }));
  });
  
  await testmu.step("Assertion check", { instructionId: "e0c3a5e7-7157-48e6-bd1f-be43d45e1f51" }, async () => {
    await testmu.verifyAssertion(page, "Assertion check", {"operator": ["equals"], "assertion_operands": [], "left_operand": null, "right_operand": null, "operands": [], "sub_results": [{"description": "Exactly two property cards remain.", "passed": true, "operator": "equals", "transforms": ["extract_number"], "json_path": null, "expected": "2", "extracted_value": "{{property_card_count_check}}", "store_key": "property_card_count_check", "variable_refs": {"{{property_card_count_check}}": "2 total properties"}}, {"description": "A Brooklyn property at $120 per night remains.", "passed": true, "operator": "equals", "transforms": [], "json_path": null, "expected": "true", "extracted_value": "{{brooklyn_property_price_check}}", "store_key": "brooklyn_property_price_check", "variable_refs": {"{{brooklyn_property_price_check}}": "true"}}, {"description": "A Scottsdale property at $145 per night remains.", "passed": true, "operator": "equals", "transforms": ["extract_number"], "json_path": null, "expected": "145", "extracted_value": "{{scottsdale_property_price_check}}", "store_key": "scottsdale_property_price_check", "variable_refs": {"{{scottsdale_property_price_check}}": "$145 night"}}], "sub_checks": [{"description": "Exactly two property cards remain.", "store_key": "property_card_count_check", "expected_value": "2", "extracted_value": "{{property_card_count_check}}", "operator": "equals", "transforms": ["extract_number"]}, {"description": "A Brooklyn property at $120 per night remains.", "store_key": "brooklyn_property_price_check", "expected_value": "true", "extracted_value": "{{brooklyn_property_price_check}}", "operator": "equals", "transforms": []}, {"description": "A Scottsdale property at $145 per night remains.", "store_key": "scottsdale_property_price_check", "expected_value": "145", "extracted_value": "{{scottsdale_property_price_check}}", "operator": "equals", "transforms": ["extract_number"]}], "composite_operator": "and", "claim": "exactly two property cards remain: a Brooklyn property at $120 per night and a Scottsdale property at $145 per night."});
  });
  
  await testmu.step("Assertion check", { instructionId: "e0094a78-c486-4639-ac1c-de8038c2bd48" }, async () => {
    await testmu.verifyAssertion(page, "Assertion check", {"operator": ["equals"], "assertion_operands": [], "left_operand": null, "right_operand": null, "operands": [], "sub_results": [{"description": "Every visible nightly price is at most $150.", "passed": true, "operator": "equals", "transforms": [], "json_path": null, "expected": "true", "extracted_value": "{{visible_nightly_prices_max_check}}", "store_key": "visible_nightly_prices_max_check", "variable_refs": {"{{visible_nightly_prices_max_check}}": "true"}}, {"description": "No $275 property is visible.", "passed": true, "operator": "equals", "transforms": [], "json_path": null, "expected": "false", "extracted_value": "{{no_275_property_visible_check}}", "store_key": "no_275_property_visible_check", "variable_refs": {"{{no_275_property_visible_check}}": "false"}}, {"description": "No $280 property is visible.", "passed": true, "operator": "equals", "transforms": [], "json_path": null, "expected": "false", "extracted_value": "{{no_280_property_visible_check}}", "store_key": "no_280_property_visible_check", "variable_refs": {"{{no_280_property_visible_check}}": "false"}}], "sub_checks": [{"description": "Every visible nightly price is at most $150.", "store_key": "visible_nightly_prices_max_check", "expected_value": "true", "extracted_value": "{{visible_nightly_prices_max_check}}", "operator": "equals", "transforms": []}, {"description": "No $275 property is visible.", "store_key": "no_275_property_visible_check", "expected_value": "false", "extracted_value": "{{no_275_property_visible_check}}", "operator": "equals", "transforms": []}, {"description": "No $280 property is visible.", "store_key": "no_280_property_visible_check", "expected_value": "false", "extracted_value": "{{no_280_property_visible_check}}", "operator": "equals", "transforms": []}], "composite_operator": "and", "claim": "every visible nightly price is at most $150 and no $275 or $280 property is visible."});
  });
  
  await testmu.step("Clicking All category filter \ud83c\udf0d All", { instructionId: "3c519f38-c096-4b4d-aab3-af76f82051ae" }, async () => {
    element_1 = page.locator("internal:role=button[name=\"\ud83c\udf0d All\"i]");
    await element_1.click();
  });
  
  await testmu.step("Reading the total property result count", async () => {
    await page.waitForLoadState("domcontentloaded", { timeout: 5000 });
    setVar("result_count_greater_than_two", await testmu.textualAnalyzer(page, { wrappedJs: "(els) => {\n  const __m = {30: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(30).textContent);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators: ["internal:text=\"total properties(Page 1 of 3)\"i"], query: "the total property result count shown above the listings", expectedValue: "2", needsUnitConversion: false, operator: "gt", transforms: ["extract_number"], condition: "The result count is greater than two." }));
  });
  
  await testmu.step("Checking for listings priced above $150 per night", async () => {
    await page.waitForLoadState("domcontentloaded", { timeout: 5000 });
    setVar("properties_above_150_appear_again", await testmu.textualAnalyzer(page, { wrappedJs: "(els) => {\n  const __m = {43: 0, 56: 1, 69: 2, 82: 3, 95: 4, 108: 5, 121: 6, 134: 7, 147: 8, 160: 9, 173: 10, 186: 11, 199: 12, 212: 13, 225: 14, 238: 15, 251: 16, 264: 17, 277: 18, 290: 19};\n  const el = (i) => els[__m[i]];\n  const __v = ([el(43),el(56),el(69),el(82),el(95),el(108),el(121),el(134),el(147),el(160),el(173),el(186),el(199),el(212),el(225),el(238),el(251),el(264),el(277),el(290)].filter(e=>Number((e.textContent.match(/\\d+/)||['0'])[0])>150).length>0);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators: ["internal:text=\"$850 night\"i", "internal:text=\"$320 night\"i", "internal:text=\"$275 night\"i", "internal:text=\"$625 night\"i", "internal:text=\"$1200 night\"i", "internal:text=\"$425 night\"i", "internal:text=\"$380 night\"i", "internal:text=\"$495 night\"i", "internal:text=\"$120 night\"i", "internal:text=\"$1500 night\"i", "internal:text=\"$180 night\"i", "internal:text=\"$195 night\"i", "internal:text=\"$340 night\"i", "internal:text=\"$890 night\"i", "internal:text=\"$280 night\"i", "internal:text=\"$395 night\"i", "internal:text=\"$145 night\"i", "internal:text=\"$750 night\"i", "internal:text=\"$285 night\"i", "internal:text=\"$580 night\"i"], query: "whether listings priced above $150 per night are present", expectedValue: "true", needsUnitConversion: false, operator: "equals", transforms: [], condition: "Properties priced above $150 appear again." }));
  });
  
  await testmu.step("Assertion check", { instructionId: "36eda849-47a0-4e47-aef2-7daba5117e04" }, async () => {
    await testmu.verifyAssertion(page, "Assertion check", {"operator": ["equals"], "assertion_operands": [], "left_operand": null, "right_operand": null, "operands": [], "sub_results": [{"description": "The result count is greater than two.", "passed": true, "operator": "gt", "transforms": ["extract_number"], "json_path": null, "expected": "2", "extracted_value": "{{result_count_greater_than_two}}", "store_key": "result_count_greater_than_two", "variable_refs": {"{{result_count_greater_than_two}}": "46 total properties(Page 1 of 3)"}}, {"description": "Properties priced above $150 appear again.", "passed": true, "operator": "equals", "transforms": [], "json_path": null, "expected": "true", "extracted_value": "{{properties_above_150_appear_again}}", "store_key": "properties_above_150_appear_again", "variable_refs": {"{{properties_above_150_appear_again}}": "true"}}], "sub_checks": [{"description": "The result count is greater than two.", "store_key": "result_count_greater_than_two", "expected_value": "2", "extracted_value": "{{result_count_greater_than_two}}", "operator": "gt", "transforms": ["extract_number"]}, {"description": "Properties priced above $150 appear again.", "store_key": "properties_above_150_appear_again", "expected_value": "true", "extracted_value": "{{properties_above_150_appear_again}}", "operator": "equals", "transforms": []}], "composite_operator": "and", "claim": "the result count is greater than two, and properties priced above $150 appear again"});
  });
});

testmu.run();
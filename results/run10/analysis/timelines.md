# Sub-task timelines

## KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it__episode_034__step_0480__trial0_open
- task: turn on the stove and put the moka pot on it
- success: True  steps: 397
- log trajectory (from sim state, not video): reach for the stove knob(0.0-3.2s) -> reach for the moka pot(3.2-11.6s) -> move the moka pot to the stove(11.6-19.9s: 夹爪闭合但未夹到物体(空抓), 达成[on moka_pot_1 flat_stove_1_cook_region])

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.2 | reach for the stove knob | T turnon flat_stove_1, F on moka_pot_1 flat_stove_1_cook_region | - |
| 64 | 3.2 | 50.5 | reach for the moka pot | T turnon flat_stove_1, F on moka_pot_1 flat_stove_1_cook_region | - |
| 232 | 11.6 | 97.3 | move the moka pot to the stove | T turnon flat_stove_1, F on moka_pot_1 flat_stove_1_cook_region | - |

**stale-progress events:**

- `moka_pot_1` from step 232 (11.6s): sub-tasks while not held = [move the moka pot to the stove] -> redo at None (delay Nones, 'None'), re-grasp executed: None, resolved_by: never

**manual trajectory (fill in after watching video):** 


## KITCHEN_SCENE4_put_the_black_bowl_in_the_bottom_drawer_of_the_cabinet_and_close_it__episode_036__step_0480__trial0_open
- task: put the black bowl in the bottom drawer of the cabinet and close it
- success: False  steps: 520
- log trajectory (from sim state, not video): grasp the black bowl(0.0-1.2s) -> push the bottom drawer closed(1.2-26.0s: 达成[close white_cabinet_1_bottom_region])

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.1 | grasp the black bowl | F close white_cabinet_1_bottom_region, F in akita_black_bowl_1 white_cabinet_1_bottom_region | - |
| 24 | 1.2 | 3.0 | push the bottom drawer closed | F close white_cabinet_1_bottom_region, F in akita_black_bowl_1 white_cabinet_1_bottom_region | - |

**stale-progress events:**

- `akita_black_bowl_1` from step 24 (1.2s): sub-tasks while not held = [push the bottom drawer closed] -> redo at None (delay Nones, 'None'), re-grasp executed: None, resolved_by: never

**manual trajectory (fill in after watching video):** 


## KITCHEN_SCENE6_put_the_yellow_and_white_mug_in_the_microwave_and_close_it__episode_038__step_0420__trial0_open
- task: put the yellow and white mug in the microwave and close it
- success: False  steps: 520
- log trajectory (from sim state, not video): reach for the yellow and white mug(0.0-0.4s) -> grasp the yellow and white mug(0.4-0.8s: 夹爪闭合但未夹到物体(空抓)) -> move the yellow and white mug to the microwave(0.8-6.0s: 夹爪闭合但未夹到物体(空抓)) -> push the microwave door closed(6.0-8.8s) -> move the yellow and white mug to the microwave(8.8-11.6s: 夹爪闭合但未夹到物体(空抓)) -> push the microwave door closed(11.6-12.8s) -> move the yellow and white mug to the microwave(12.8-16.0s: 夹爪闭合但未夹到物体(空抓)) -> release the yellow and white mug(16.0-16.4s) -> push the microwave door closed(16.4-18.0s) -> move the yellow and white mug to the microwave(18.0-19.6s: 夹爪闭合但未夹到物体(空抓)) -> push the microwave door closed(19.6-26.0s)

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.1 | reach for the yellow and white mug | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 8 | 0.4 | 1.1 | grasp the yellow and white mug | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 16 | 0.8 | 1.9 | move the yellow and white mug to the microwave | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 120 | 6.0 | 16.3 | push the microwave door closed | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 176 | 8.8 | 22.5 | move the yellow and white mug to the microwave | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 232 | 11.6 | 30.3 | push the microwave door closed | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 256 | 12.8 | 33.3 | move the yellow and white mug to the microwave | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 320 | 16.0 | 42.5 | release the yellow and white mug | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 328 | 16.4 | 43.6 | push the microwave door closed | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 360 | 18.0 | 47.5 | move the yellow and white mug to the microwave | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |
| 392 | 19.6 | 52.5 | push the microwave door closed | T in white_yellow_mug_1 microwave_1_heating_region, F close microwave_1 | - |

**manual trajectory (fill in after watching video):** 


## KITCHEN_SCENE8_put_both_moka_pots_on_the_stove__episode_002__step_0420__trial0_open
- task: put both moka pots on the stove
- success: False  steps: 520
- log trajectory (from sim state, not video): reach for the first moka pot(0.0-7.2s) -> reach for the second moka pot(7.2-9.2s) -> reach for the first moka pot(9.2-12.8s) -> reach for the second moka pot(12.8-16.0s) -> reach for the first moka pot(16.0-17.6s) -> reach for the second moka pot(17.6-26.0s)

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.1 | reach for the first moka pot | F on moka_pot_1 flat_stove_1_cook_region, F on moka_pot_2 flat_stove_1_cook_region, T turnon flat_stove_1 | - |
| 144 | 7.2 | 17.5 | reach for the second moka pot | F on moka_pot_1 flat_stove_1_cook_region, F on moka_pot_2 flat_stove_1_cook_region, T turnon flat_stove_1 | - |
| 184 | 9.2 | 22.5 | reach for the first moka pot | F on moka_pot_1 flat_stove_1_cook_region, F on moka_pot_2 flat_stove_1_cook_region, T turnon flat_stove_1 | - |
| 256 | 12.8 | 32.0 | reach for the second moka pot | F on moka_pot_1 flat_stove_1_cook_region, F on moka_pot_2 flat_stove_1_cook_region, T turnon flat_stove_1 | - |
| 320 | 16.0 | 40.9 | reach for the first moka pot | F on moka_pot_1 flat_stove_1_cook_region, F on moka_pot_2 flat_stove_1_cook_region, T turnon flat_stove_1 | - |
| 352 | 17.6 | 45.5 | reach for the second moka pot | F on moka_pot_1 flat_stove_1_cook_region, F on moka_pot_2 flat_stove_1_cook_region, T turnon flat_stove_1 | - |

**manual trajectory (fill in after watching video):** 


## LIVING_ROOM_SCENE1_put_both_the_alphabet_soup_and_the_cream_cheese_box_in_the_basket__episode_037__step_0480__trial0_open
- task: put both the alphabet soup and the cream cheese box in the basket
- success: False  steps: 520
- log trajectory (from sim state, not video): reach for the alphabet soup(0.0-6.4s) -> grasp the alphabet soup(6.4-6.8s) -> move the alphabet soup to the basket(6.8-8.8s: 夹爪闭合但未夹到物体(空抓)) -> release the alphabet soup(8.8-9.2s) -> reach for the cream cheese box(9.2-12.8s) -> grasp the cream cheese box(12.8-13.2s: 抓住cream_cheese_1) -> move the cream cheese box to the basket(13.2-15.6s: 抓住cream_cheese_1, cream_cheese_1被抬起23cm) -> release the cream cheese box(15.6-26.0s: 抓住cream_cheese_1, cream_cheese_1被抬起16cm, 松开/掉落cream_cheese_1)

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.1 | reach for the alphabet soup | F in alphabet_soup_1 basket_1_contain_region, F in cream_cheese_1 basket_1_contain_region | - |
| 128 | 6.4 | 14.9 | grasp the alphabet soup | F in alphabet_soup_1 basket_1_contain_region, F in cream_cheese_1 basket_1_contain_region | - |
| 136 | 6.8 | 15.8 | move the alphabet soup to the basket | F in alphabet_soup_1 basket_1_contain_region, F in cream_cheese_1 basket_1_contain_region | - |
| 176 | 8.8 | 21.5 | release the alphabet soup | F in alphabet_soup_1 basket_1_contain_region, F in cream_cheese_1 basket_1_contain_region | - |
| 184 | 9.2 | 22.3 | reach for the cream cheese box | F in alphabet_soup_1 basket_1_contain_region, F in cream_cheese_1 basket_1_contain_region | - |
| 256 | 12.8 | 31.2 | grasp the cream cheese box | F in alphabet_soup_1 basket_1_contain_region, F in cream_cheese_1 basket_1_contain_region | - |
| 264 | 13.2 | 32.1 | move the cream cheese box to the basket | F in alphabet_soup_1 basket_1_contain_region, F in cream_cheese_1 basket_1_contain_region | cream_cheese_1 |
| 312 | 15.6 | 38.6 | release the cream cheese box | F in alphabet_soup_1 basket_1_contain_region, F in cream_cheese_1 basket_1_contain_region | cream_cheese_1 |

**stale-progress events:**

- `alphabet_soup_1` from step 136 (6.8s): sub-tasks while not held = [move the alphabet soup to the basket | release the alphabet soup | reach for the cream cheese box | grasp the cream cheese box | move the cream cheese box to the basket | release the cream cheese box] -> redo at None (delay Nones, 'None'), re-grasp executed: None, resolved_by: never
- `cream_cheese_1` from step 320 (16.0s): sub-tasks while not held = [release the cream cheese box] -> redo at None (delay Nones, 'None'), re-grasp executed: None, resolved_by: never

**manual trajectory (fill in after watching video):** 


## LIVING_ROOM_SCENE2_put_both_the_alphabet_soup_and_the_tomato_sauce_in_the_basket__episode_000__step_0480__trial0_open
- task: put both the alphabet soup and the tomato sauce in the basket
- success: True  steps: 292
- log trajectory (from sim state, not video): reach for the alphabet soup(0.0-4.0s: 抓住alphabet_soup_1) -> grasp the alphabet soup(4.0-4.4s: 抓住alphabet_soup_1) -> move the alphabet soup to the basket(4.4-8.0s: 抓住alphabet_soup_1, alphabet_soup_1被抬起22cm) -> release the alphabet soup(8.0-8.4s: alphabet_soup_1被抬起12cm, 达成[in alphabet_soup_1 basket_1_contain_region]) -> reach for the tomato sauce(8.4-11.6s) -> grasp the tomato sauce(11.6-12.0s: 抓住tomato_sauce_1) -> move the tomato sauce to the basket(12.0-14.4s: 抓住tomato_sauce_1, tomato_sauce_1被抬起24cm) -> release the tomato sauce(14.4-14.6s: 抓住tomato_sauce_1, tomato_sauce_1被抬起11cm, 松开/掉落tomato_sauce_1, 达成[in tomato_sauce_1 basket_1_contain_region])

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.1 | reach for the alphabet soup | F in alphabet_soup_1 basket_1_contain_region, F in tomato_sauce_1 basket_1_contain_region | - |
| 80 | 4.0 | 9.1 | grasp the alphabet soup | F in alphabet_soup_1 basket_1_contain_region, F in tomato_sauce_1 basket_1_contain_region | alphabet_soup_1 |
| 88 | 4.4 | 10.2 | move the alphabet soup to the basket | F in alphabet_soup_1 basket_1_contain_region, F in tomato_sauce_1 basket_1_contain_region | alphabet_soup_1 |
| 160 | 8.0 | 19.1 | release the alphabet soup | F in alphabet_soup_1 basket_1_contain_region, F in tomato_sauce_1 basket_1_contain_region | alphabet_soup_1 |
| 168 | 8.4 | 20.1 | reach for the tomato sauce | T in alphabet_soup_1 basket_1_contain_region, F in tomato_sauce_1 basket_1_contain_region | - |
| 232 | 11.6 | 27.5 | grasp the tomato sauce | T in alphabet_soup_1 basket_1_contain_region, F in tomato_sauce_1 basket_1_contain_region | - |
| 240 | 12.0 | 28.6 | move the tomato sauce to the basket | T in alphabet_soup_1 basket_1_contain_region, F in tomato_sauce_1 basket_1_contain_region | tomato_sauce_1 |
| 288 | 14.4 | 34.7 | release the tomato sauce | T in alphabet_soup_1 basket_1_contain_region, F in tomato_sauce_1 basket_1_contain_region | tomato_sauce_1 |

**manual trajectory (fill in after watching video):** 


## LIVING_ROOM_SCENE2_put_both_the_cream_cheese_box_and_the_butter_in_the_basket__episode_001__step_0440__trial0_open
- task: put both the cream cheese box and the butter in the basket
- success: False  steps: 520
- log trajectory (from sim state, not video): reach for the cream cheese box(0.0-1.2s) -> move the cream cheese box to the basket(1.2-2.4s: 夹爪闭合但未夹到物体(空抓)) -> reach for the cream cheese box(2.4-2.8s) -> reach for the butter(2.8-3.2s) -> move the cream cheese box to the basket(3.2-3.6s) -> release the cream cheese box(3.6-4.0s) -> reach for the cream cheese box(4.0-4.4s) -> move the cream cheese box to the basket(4.4-7.6s: 夹爪闭合但未夹到物体(空抓)) -> release the cream cheese box(7.6-8.0s) -> reach for the butter(8.0-10.4s: 抓住butter_1) -> move the butter to the basket(10.4-10.8s: 抓住butter_1, butter_1被抬起5cm, 松开/掉落butter_1) -> release the butter(10.8-11.2s) -> reach for the butter(11.2-12.4s: butter_1飞出场景(仿真异常)) -> grasp the cream cheese box(12.4-12.8s: butter_1飞出场景(仿真异常)) -> grasp the butter(12.8-13.2s: 夹爪闭合但未夹到物体(空抓), butter_1飞出场景(仿真异常)) -> move the cream cheese box to the basket(13.2-15.6s: 夹爪闭合但未夹到物体(空抓), butter_1飞出场景(仿真异常)) -> move the butter to the basket(15.6-16.0s: 夹爪闭合但未夹到物体(空抓)) -> release the butter(16.0-16.4s) -> reach for the butter(16.4-18.4s) -> pull the butter to the basket(18.4-18.8s) -> release the butter(18.8-19.2s) -> reach for the butter(19.2-21.6s) -> grasp the cream cheese box(21.6-22.0s) -> grasp the butter(22.0-22.4s: 夹爪闭合但未夹到物体(空抓)) -> move the butter to the basket(22.4-24.4s: 夹爪闭合但未夹到物体(空抓)) -> move the cream cheese box to the basket(24.4-24.8s: 夹爪闭合但未夹到物体(空抓)) -> move the butter to the basket(24.8-25.6s: 夹爪闭合但未夹到物体(空抓)) -> release the butter(25.6-26.0s)

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.1 | reach for the cream cheese box | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 24 | 1.2 | 2.8 | move the cream cheese box to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 48 | 2.4 | 6.0 | reach for the cream cheese box | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 56 | 2.8 | 6.9 | reach for the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 64 | 3.2 | 7.9 | move the cream cheese box to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 72 | 3.6 | 9.0 | release the cream cheese box | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 80 | 4.0 | 9.8 | reach for the cream cheese box | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 88 | 4.4 | 10.8 | move the cream cheese box to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 152 | 7.6 | 18.7 | release the cream cheese box | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 160 | 8.0 | 19.5 | reach for the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 208 | 10.4 | 24.9 | move the butter to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | butter_1 |
| 216 | 10.8 | 25.8 | release the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 224 | 11.2 | 26.6 | reach for the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 248 | 12.4 | 29.5 | grasp the cream cheese box | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 256 | 12.8 | 30.4 | grasp the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 264 | 13.2 | 31.3 | move the cream cheese box to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 312 | 15.6 | 37.5 | move the butter to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 320 | 16.0 | 38.5 | release the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 328 | 16.4 | 39.3 | reach for the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 368 | 18.4 | 44.3 | pull the butter to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 376 | 18.8 | 45.3 | release the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 384 | 19.2 | 46.2 | reach for the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 432 | 21.6 | 52.6 | grasp the cream cheese box | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 440 | 22.0 | 53.6 | grasp the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 448 | 22.4 | 54.9 | move the butter to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 488 | 24.4 | 60.7 | move the cream cheese box to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 496 | 24.8 | 62.0 | move the butter to the basket | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |
| 512 | 25.6 | 64.2 | release the butter | F in cream_cheese_1 basket_1_contain_region, F in butter_1 basket_1_contain_region | - |

**stale-progress events:**

- `cream_cheese_1` from step 24 (1.2s): sub-tasks while not held = [move the cream cheese box to the basket] -> redo at 48 (delay 1.2s, 'reach for the cream cheese box'), re-grasp executed: False, resolved_by: redo
- `cream_cheese_1` from step 64 (3.2s): sub-tasks while not held = [move the cream cheese box to the basket | release the cream cheese box] -> redo at 80 (delay 0.8s, 'reach for the cream cheese box'), re-grasp executed: False, resolved_by: redo
- `cream_cheese_1` from step 88 (4.4s): sub-tasks while not held = [move the cream cheese box to the basket | release the cream cheese box | reach for the butter | move the butter to the basket | release the butter] -> redo at 248 (delay 8.0s, 'grasp the cream cheese box'), re-grasp executed: False, resolved_by: redo
- `cream_cheese_1` from step 264 (13.2s): sub-tasks while not held = [move the cream cheese box to the basket | move the butter to the basket | release the butter | reach for the butter | pull the butter to the basket] -> redo at 432 (delay 8.4s, 'grasp the cream cheese box'), re-grasp executed: False, resolved_by: redo
- `cream_cheese_1` from step 488 (24.4s): sub-tasks while not held = [move the cream cheese box to the basket | move the butter to the basket | release the butter] -> redo at None (delay Nones, 'None'), re-grasp executed: None, resolved_by: never
- `butter_1` from step 216 (10.8s): sub-tasks while not held = [release the butter] -> redo at 224 (delay 0.4s, 'reach for the butter'), re-grasp executed: False, resolved_by: redo
- `butter_1` from step 248 (12.4s): sub-tasks while not held = [grasp the cream cheese box] -> redo at 256 (delay 0.4s, 'grasp the butter'), re-grasp executed: False, resolved_by: redo
- `butter_1` from step 264 (13.2s): sub-tasks while not held = [move the cream cheese box to the basket | move the butter to the basket | release the butter] -> redo at 328 (delay 3.2s, 'reach for the butter'), re-grasp executed: False, resolved_by: redo
- `butter_1` from step 376 (18.8s): sub-tasks while not held = [release the butter] -> redo at 384 (delay 0.4s, 'reach for the butter'), re-grasp executed: False, resolved_by: redo
- `butter_1` from step 432 (21.6s): sub-tasks while not held = [grasp the cream cheese box] -> redo at 440 (delay 0.4s, 'grasp the butter'), re-grasp executed: False, resolved_by: redo
- `butter_1` from step 448 (22.4s): sub-tasks while not held = [move the butter to the basket | move the cream cheese box to the basket | release the butter] -> redo at None (delay Nones, 'None'), re-grasp executed: None, resolved_by: never

**manual trajectory (fill in after watching video):** 


## LIVING_ROOM_SCENE5_put_the_white_mug_on_the_left_plate_and_put_the_yellow_and_white_mug_on_the_right_plate__episode_024__step_0500__trial0_open
- task: put the white mug on the left plate and put the yellow and white mug on the right plate
- success: False  steps: 520
- log trajectory (from sim state, not video): reach for the white mug(0.0-11.6s) -> reach for the yellow and white mug(11.6-12.0s) -> reach for the white mug(12.0-15.2s) -> reach for the yellow and white mug(15.2-17.6s) -> reach for the white mug(17.6-18.0s) -> reach for the yellow and white mug(18.0-26.0s)

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.1 | reach for the white mug | F on porcelain_mug_1 plate_1, F on white_yellow_mug_1 plate_2 | - |
| 232 | 11.6 | 27.0 | reach for the yellow and white mug | F on porcelain_mug_1 plate_1, F on white_yellow_mug_1 plate_2 | - |
| 240 | 12.0 | 28.1 | reach for the white mug | F on porcelain_mug_1 plate_1, F on white_yellow_mug_1 plate_2 | - |
| 304 | 15.2 | 36.3 | reach for the yellow and white mug | F on porcelain_mug_1 plate_1, F on white_yellow_mug_1 plate_2 | - |
| 352 | 17.6 | 43.2 | reach for the white mug | F on porcelain_mug_1 plate_1, F on white_yellow_mug_1 plate_2 | - |
| 360 | 18.0 | 44.3 | reach for the yellow and white mug | F on porcelain_mug_1 plate_1, F on white_yellow_mug_1 plate_2 | - |

**manual trajectory (fill in after watching video):** 


## LIVING_ROOM_SCENE6_put_the_white_mug_on_the_plate_and_put_the_chocolate_pudding_to_the_right_of_the_plate__episode_039__step_0400__trial0_open
- task: put the white mug on the plate and put the chocolate pudding to the right of the plate
- success: False  steps: 520
- log trajectory (from sim state, not video): reach for the white mug(0.0-20.4s) -> reach for the chocolate pudding(20.4-21.2s) -> release the white mug(21.2-21.6s) -> reach for the chocolate pudding(21.6-24.0s) -> release the white mug(24.0-24.4s) -> reach for the chocolate pudding(24.4-26.0s)

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.1 | reach for the white mug | F on porcelain_mug_1 plate_1, F on chocolate_pudding_1 living_room_table_plate_right_region | - |
| 408 | 20.4 | 49.0 | reach for the chocolate pudding | F on porcelain_mug_1 plate_1, F on chocolate_pudding_1 living_room_table_plate_right_region | - |
| 424 | 21.2 | 50.9 | release the white mug | F on porcelain_mug_1 plate_1, F on chocolate_pudding_1 living_room_table_plate_right_region | - |
| 432 | 21.6 | 52.0 | reach for the chocolate pudding | F on porcelain_mug_1 plate_1, F on chocolate_pudding_1 living_room_table_plate_right_region | - |
| 480 | 24.0 | 58.8 | release the white mug | F on porcelain_mug_1 plate_1, F on chocolate_pudding_1 living_room_table_plate_right_region | - |
| 488 | 24.4 | 60.1 | reach for the chocolate pudding | F on porcelain_mug_1 plate_1, F on chocolate_pudding_1 living_room_table_plate_right_region | - |

**stale-progress events:**

- `porcelain_mug_1` from step 424 (21.2s): sub-tasks while not held = [release the white mug | reach for the chocolate pudding] -> redo at None (delay Nones, 'None'), re-grasp executed: None, resolved_by: never

**manual trajectory (fill in after watching video):** 


## STUDY_SCENE1_pick_up_the_book_and_place_it_in_the_back_compartment_of_the_caddy__episode_020__step_0400__trial0_open
- task: pick up the book and place it in the back compartment of the caddy
- success: False  steps: 520
- log trajectory (from sim state, not video): reach for the book(0.0-4.4s) -> grasp the book(4.4-5.2s: 夹爪闭合但未夹到物体(空抓)) -> move the book to the back compartment of the caddy(5.2-14.4s: 夹爪闭合但未夹到物体(空抓)) -> release the book(14.4-17.2s) -> reach for the book(17.2-17.6s) -> release the book(17.6-22.0s) -> reach for the book(22.0-22.4s) -> release the book(22.4-26.0s)

| step | t(s) | wall(s) | sub-task | goal | grasped |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.1 | reach for the book | F in black_book_1 desk_caddy_1_back_contain_region | - |
| 88 | 4.4 | 8.9 | grasp the book | F in black_book_1 desk_caddy_1_back_contain_region | - |
| 104 | 5.2 | 10.3 | move the book to the back compartment of the caddy | F in black_book_1 desk_caddy_1_back_contain_region | - |
| 288 | 14.4 | 38.1 | release the book | F in black_book_1 desk_caddy_1_back_contain_region | - |
| 344 | 17.2 | 43.9 | reach for the book | F in black_book_1 desk_caddy_1_back_contain_region | - |
| 352 | 17.6 | 44.9 | release the book | F in black_book_1 desk_caddy_1_back_contain_region | - |
| 440 | 22.0 | 55.3 | reach for the book | F in black_book_1 desk_caddy_1_back_contain_region | - |
| 448 | 22.4 | 56.4 | release the book | F in black_book_1 desk_caddy_1_back_contain_region | - |

**stale-progress events:**

- `black_book_1` from step 104 (5.2s): sub-tasks while not held = [move the book to the back compartment of the caddy | release the book] -> redo at 344 (delay 12.0s, 'reach for the book'), re-grasp executed: False, resolved_by: redo
- `black_book_1` from step 352 (17.6s): sub-tasks while not held = [release the book] -> redo at 440 (delay 4.4s, 'reach for the book'), re-grasp executed: False, resolved_by: redo
- `black_book_1` from step 448 (22.4s): sub-tasks while not held = [release the book] -> redo at None (delay Nones, 'None'), re-grasp executed: None, resolved_by: never

**manual trajectory (fill in after watching video):** 


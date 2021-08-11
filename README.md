# INTERPRET Multi-Agent Prediction and Conditional Multi-Agent Prediction

In the Multi-Agent Prediction and Conditional Multi-Agent Prediction track, the target is to jointly predict multiple target agents' **coordinates and yaw** in the future 3 seconds (30 frames). All target agents are fully observable during the 1+3 seconds. Regarding the yaw prediction, please refer to the Regarding the Predicted Yaw Angle of this page.

## Submission Policy
The provided training data of the INTERPRET challenge may be used for learning the parameters of the algorithms. The test data should be used strictly for reporting the final results compared to competitors on the INTERPRET website - it must not be used in any way to train or tune the systems, for example by evaluating multiple parameters or feature choices and reporting the best results obtained. We have provided a suggested split between the training and validation sets using the INTERACTION drone dataset, and the participants can choose to use that. The tuned algorithms should then be run only once on the test data.

The evaluation server may not be used for parameter tuning. We allow participants to upload the results of their algorithm onto the server and perform all other experiments on the training and validation set.

The trajectory prediction results will be evaluated automatically and participants can decide whether each evaluation result is public in their submission log pages. The default is non-public.

## Data Format

For each csv file in the released "train" and "val" folder, the csv's name represents the scene name.  Each csv file includes multiple cases and each case includes all agents' states in 4 seconds. Note that some agents may not be fully visible in the 4 seconds. In the csv file, each row represents a agent's state at a timestamp of a case and each columns means:

case id: the id of the case under this driving scenario.

track_id: the agent id.

frame_id: the id of the current frame.

timestamp_ms: the time instant of the corresponding frame in ms.

agent_type: the type of the agent. It is either "car" or "pedestrian/bicycle".

x: the x position of the agent. Unit: m. The coordinate system of the agent is a relative coordinate system with respect to some predefined points in our recorded scenes.

y: the x position of the agent. Unit: m. The coordinate system of the agent is a relative coordinate system with respect to some predefined points in our recorded scenes.

vx: the velocity in the x-direction of the agent. Unit: m/s.

vy: the velocity in the y-direction of the agent. Unit: m/s.

psi_rad: the yaw angle of the agent if the agent is a vehicle. If the agent is a pedestrian, then this column is empty. Unit: rad.

length: the length(size) of the agent if the agent is a vehicle. If the agent is a pedestrian, then this column is empty. Unit: m.

width: the width(size) of the agent if the agent is a vehicle. If the agent is a pedestrian, then this column is empty. Unit: m.


For each csv file in the released "test_multi-agent" and "test_conditional-multi-agent" folder, since they are the input data of the competition, there are the following differences:

1. There are only 1 second observation of each case. The future 3 seconds is the prediction horizon.
 
2. Additional columns:  "interesting agent" indicates whether a vehicle is the ego agent of the case where 0 means no and 1 means yes. Each case only has one "interesting agent".  "track_to_predict" indicates whether a vehicle is a target agent for the trajectory prediction. All target agents are guaranteed to be fully observable in the 1+3 seconds of the raw data. Only vehicles are selected as the ego agent or the target agent.  Regarding how the columns are labeled please check the [main page of the competition](http://challenge.interaction-dataset.com/prediction-challenge/intro). Participants are free to decide the strategy of setting "interesting agent" and  "track_to_predict" in the train/val data.


## Submission

For each scenario X like (DR_CHN_Merging_ZS0) of each track, there should be a single file 'X_sub.csv'. The following columns would be used during the evaluation: case_id, track_id, frame_id, timestamp_ms, track_to_predict, interesting_agent, x1, y1, psi_rad1, x2, y2, psi_rad2, x3, y3, psi_rad3, x4, y4, psi_rad4, x5, y5, psi_rad5, x6, y6, psi_rad6. Other columns would be ignored. The order of rows and columns could be arbitrary. 'xi, yi, psi_radi' represents the predicted coordinate and yaw for the vehicle 'track_id' at 'timestamp_ms' in the modality i. Up to 6 modalities would be taken into consideration. Participants could submit less than 6 modalities (like only x1, y1, psi_rad1). All agents in the input data with the 'track_to_predict' column as 1 should has predictions for 30 timestamps. Each submission could contain up to 6 modalities where the modality with higher confidence should has smaller index. In other words, modalaity 1 has the highest confidence and modality 6 has the lowest. Note that participants should upload the ego agnet ("interesting_agent")'s predictions since its "track_to_predict" column is 1. However, the ego agnet's predictions would be excluded in all metrics. Thus, participants are free to upload arbitrary value of (x, y, yaw) which should have equal number of modalities with other "track_to_predict". It only serves as data alignment.

Csv files for all scenarios of a track should be packed into **a single zip** file for submission.

[DR_CHN_Merging_ZS0_sub.csv](https://github.com/interaction-dataset/INTERPRET_challenge_multi-agent/blob/main/DR_CHN_Merging_ZS0_sub.csv) is an example for submission for the scenario DR_CHN_Merging_ZS0. Note that this example file only contains 3 cases and the input is random number.


## Metrics
All metrics are averaged over all cases of all scenarios. The ranking of both tracks is based on the **Consistent-minJointMR**.

### minJointADE
Minimum Joint Average Displacement Error (minJointADE) represents the minimum value of the euclid distance averaged by time and all agents between the ground truth and modality with the lowest value. The minJointADE of a single case is calculated as:

![](http://latex.codecogs.com/gif.latex?\\text{minJointADE}=\\min\\limits_{k\\in\\{1,...,K\\}}\\frac1{NT}\\sum\\limits_{n,t}\\sqrt{(\\hat{x}_{n,t}-x_{n,t}^k)^2+(\\hat{y}_{n,t}-y_{n,t}^k)^2})



where N is the number of agents to be predicted in this case, T is the number of predicted timestamps which is 30 in this challenge, K is the number of modalities in this challenge, $\hat{x}$ and $\hat{y}$ means the ground truth. The final value is averaged over all cases.

Note that this metric excludes the interesting agent in the evaluation process because in the practical application the prediction stage serves for the planning stage and there is no need to predict the ego agent.

### minJointFDE
Minimum Joint Final Displacement Error (minJointFDE) represents the minimum value of the euclid distance at the last predicted timestamps averaged by all agents between the ground truth and modality with the lowest value. The minJointFDE of a single case is calculated as:

![](http://latex.codecogs.com/gif.latex?\\text{minJointFDE}=\\min\\limits_{k\\in\\{1,...,K\\}}\\frac1{N}\\sum\\limits_{n}\\sqrt{(\\hat{x}_{n,T}-x_{n,T}^k)^2+(\\hat{y}_{n,T}-y_{n,T}^k)^2})

where N is the number of agents to be predicted in this case, T is the final predicted timestamps which is 30 in this challenge, K is the number of modalities in this challenge, $\hat{x}$ and $\hat{y}$ means the ground truth. The final value is averaged over all cases.

Similar to the minJointADE, this metric excludes the interesting agent in the evaluation process.


### CrossCollisionRate
Cross Collision Rate represents the frequency of collisions happening among the predictions in each modalaity. It is a value between 0~1. For a modality of a case, excluding the interesting vehicle, if there is **any** of the two vehciles has collisions at **any** timestampes, this modality is considered as 'having collosion'. Then, for the 6 modalities of a case, we calculate the ratio of collosion happening by collision_num/6 where collosion_num is between 0 and 6. The final value is averaged over all cases.

This metric is to evaluate the consistency of the joint prediction in each modality. It punishes the predictions where there is collosions in their predictions.

Note that we **do not consider** the collisions between the interesting agent and other agents because in the practical application the prediction stage serves for the planning stage and the future motion of the ego agent should be decided by the planning stage.
 
##### Collision Detection Process
Instead of simply considering each vehicle as a point, we consider the length and width of the vehicle in the collision detection process. We use a list of circles to represent a vehicle at each timestamp.  If the distance between any two circles' origins of the given two vehicles is lower than a threshold, it is considered as they have a collision at that timestamp. [calculate_collision.py ](https://github.com/interaction-dataset/INTERPRET_challenge_multi-agent/blob/main/calculate_collision.py) includes a function which could output the circle lists for a given vehicle and a function which could output the collision threshold of two vehicles.

### EgoCollisionRate
Ego Collision Rate represents the collisions happening between the **ground truth** of the interesting agent and the **predictions** in each case.  It is a value between 0~1. For a modality of a case, if there is a collision between the ground truth of the interesting agent and **any** of other agents' predictions at **any** timestampes, this modality is considered as 'having collosion'. If **at least one** modality does not have collisions, then the case is considered to be 'no collision' - 0. Otherwise, the case is considered as 'having collision' - 1. The final value is averaged over all cases.

This metric is to evluate whether the prediction model could give at least one modality of other agents where the ego agent in the ground truth modality could successfully pass. If the model fails to do so, its multi-modal prediction is trouble-some for the planning stage.

### minJointMR

For a vehicle in a modality of a case, if its prediction at the final timestamp T=30 is out of a given lateral or longitudinal threshold of the ground truth, it is considered as 'miss'. Specifically, we first rotate the groud truth and the prediction according to the ground truth yaw angle at T=30 so that the x-axis is the longitudinal direction and the y-axis is the lateral direction. The lateral threshold is set as 1 meter and the longitudinal is set as a piecewise function based on the velocity v of the ego agent's ground truth at T=30. For the high-speed scenario, the funcition gives a larger longitudinal threshold.


<img src="https://latex.codecogs.com/svg.image?\text{Threshold}_\text{lon}=\left\{\begin{matrix}1&space;&&space;v<1.4m/s&space;\\1&plus;\frac{v-1.4}{v-11}&space;&space;&&space;1.4m/s&space;\leq&space;v&space;\leq&space;11m/s\\2&space;&&space;v&space;\geq&space;11m/s&space;\\\end{matrix}\right." title="\text{Threshold}_\text{lon}=\left\{\begin{matrix}1 & v<1.4m/s \\1+\frac{v-1.4}{v-11} & 1.4m/s \leq v \leq 11m/s\\2 & v \geq 11m/s \\\end{matrix}\right." />

If the lateral or longitudinal distance between the prediction and ground truth at the last timestamp is larger than the cooresponding threshold, this vehicle in this modality of this case is considered as 'miss' - 1.

To calculate Minimum Joint Miss Rate (minJointMR), we first calculate the ratio of miss for each modality, i.e., number_of_miss_in_one_modality/number_of_other_agents. Then, we take the minimum MR over all modalities as the case's MR - minJointMR. The final value is averaged over all cases.

Similar to minJointADE and minJointFDE, we do not calculate the ego agent's MR in the whole evaluation process.

### Consistent-minJointMR
Consistent-minJointMR has the same computation process except that when taking the minimum MR over all modalities as the case's MR, we only consider those modalities without CrossCollision. If all modalities have collisions, this case's Consistent-minJointMR is considered as 1 directly.

This metric is to encourge the prediction model to make consistent predictions. If a modality in its prediction contains collisions, it 'wastes' this attempt. It is the ranking metric.

## Regarding the Predicted Yaw Angle
Many motion prediction models only output x and y. In this challenge, since the collision detecton has taken the vehicles' length and width into consideration, we need the vehicles' yaw angle as well. We strongly suggest the participants to visualize their predictions in the form of the bounding box. If the yaw angle is calculated by first taking difference over time to get velocity and then taking the arctan to obtain yaw, the unsmoothed yaw angle may cause collisions.

# Note
For guidance of **INTERPRET Single Agent Prediction and Conditional Single Agent Prediction in the ICCV21 Stage**, please visit https://github.com/interaction-dataset/INTERPRET_challenge_single-agent.


## Acknowledgement
Some metrics are inspired by the [Waymo Open Dataset - Motion Prediction Challenge](https://waymo.com/open/challenges/2021/motion-prediction/) and [Argoverse Motion Forecasting Competition](https://eval.ai/web/challenges/challenge-page/454/overview).

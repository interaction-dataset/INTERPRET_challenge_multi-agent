# INTERPRET Multi-Agent Track

In this track, the input is M agents' motion information including coordinates, velocities, yaw, vehicle length and width in the observed 1 second (10 frames) as well as the cooresponding HD map. The target is to predict N (<= M) agents' coordinates and yaw in the future 3 seconds (30 frames). Note that the N agents are selected because they are fully observable during the 1+3 seconds. In addition, one of the N agents is denoted as the 'interesting agent' (csv column 'interesting_agent' as 1) to serve as the ego agent during the evaluation process. 

## Submission
Please first read [the guideline of the single agnet track](http://challenge.interaction-dataset.com/leader-board-introduction) for the basic information about the input data and submission. Most of them still applies in the multi-agent track.

The following are the changed parts in the multi-agent track:

For each scenario X like (DR_CHN_Merging_ZS0), there should be a single file 'X_sub.csv'. The following columns would be used during the evaluation: case_id, track_id, frame_id, timestamp_ms, x1, y1, psi_rad1, x2, y2, psi_rad2, x3, y3, psi_rad3, x4, y4, psi_rad4, x5, y5, psi_rad5, x6, y6, psi_rad6. The order of rows and columns could be arbitrary. 'xi, yi, psi_radi' represents the predicted coordinate and yaw for the vehicle 'track_id' at 'timestamp_ms' in the modality i. Up to 6 modalities would be taken into consideration. Participants could submit less than 6 modalities (like only x1, y1, psi_rad1).

All vehicles in the input data with the 'track_to_predict' column as 1 should has predictions for 30 timestamps. Each submission could contain up to 6 modalities where the modality with higher confidence should has smaller index. In other words, modalaity 1 has the highest confidence and modality 6 has the lowest.

Csv files for all scenarios should be packed into **a single zip** file for submission.

[DR_CHN_Merging_ZS0_sub.csv](https://github.com/interaction-dataset/INTERPRET_challenge_multi-agent/blob/main/DR_CHN_Merging_ZS0_sub.csv) is an example for submission for the scenario DR_CHN_Merging_ZS0. Note that this example file only contains 3 cases and the input is random number.

## Metrics
All metrics are averaged over all cases of all scenarios. The ranking of the challenge is based on the **Consistent-minJointMR**.

### minJointADE
Minimum Joint Average Displacement Error (minJointADE) represents the minimum value of the euclid distance averaged by time and all agents between the ground truth and modality with the lowest value. The minJointADE of a single case is calculated as:

![](http://latex.codecogs.com/gif.latex?\\text{minJointADE}=\\min\\limits_{k\\in\\{1,...,K\\}}\\frac1{NT}\\sum\\limits_{n,t}\\sqrt{(\\hat{x}_{n,t}-x_{n,t}^k)^2+(\\hat{y}_{n,t}-y_{n,t}^k)^2})



where N is the number of agents to be predicted in this case, T is the number of predicted timestamps which is 30 in this challenge, K is the number of modalities which is 6 in this challenge, $\hat{x}$ and $\hat{y}$ means the ground truth. The final value is averaged over all cases.

Note that this metric excludes the interesting agent in the evaluation process because in the practical application the prediction stage serves for the planning stage and there is no need to predict the ego agent.

### minJointFDE
Minimum Joint Final Displacement Error (minJointFDE) represents the minimum value of the euclid distance at the last predicted timestamps averaged by all agents between the ground truth and modality with the lowest value. The minJointFDE of a single case is calculated as:

![](http://latex.codecogs.com/gif.latex?\\text{minJointFDE}=\\min\\limits_{k\\in\\{1,...,K\\}}\\frac1{N}\\sum\\limits_{n}\\sqrt{(\\hat{x}_{n,T}-x_{n,T}^k)^2+(\\hat{y}_{n,T}-y_{n,T}^k)^2})

where N is the number of agents to be predicted in this case, T is the final predicted timestamps which is 30 in this challenge, K is the number of modalities which is 6 in this challenge, $\hat{x}$ and $\hat{y}$ means the ground truth. The final value is averaged over all cases.

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

This metric is to encourge the prediction model to make consistent predictions. If a modality in its prediction contains collisions, it 'wastes' this attempt. It is the ranking metric for the challenge.

### Regarding the Predicted Yaw Angle
Many motion prediction models only output x and y. In this challenge, since the collision detecton has taken the vehicles' length and width into consideration, we need the vehicles' yaw angle as well. We strongly suggest the participants to visualize their predictions in the form of the bounding box. If the yaw angle is calculated by first taking difference over time to get velocity and then taking the arctan to obtain yaw, the unsmoothed yaw angle may cause collisions.

### Acknowledgement
Some metrics are inspired by the [Waymo Open Dataset - Motion Prediction Challenge](https://waymo.com/open/challenges/2021/motion-prediction/) and [Argoverse Motion Forecasting Competition](https://eval.ai/web/challenges/challenge-page/454/overview).
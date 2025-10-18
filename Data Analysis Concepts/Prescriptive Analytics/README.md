<h1 align="center">Prescriptive Analytics</h1>

<p align="center">
  Prescriptive analytics represents the most advanced stage of data analysis, focusing not only on predicting future outcomes but also recommending optimal decisions and actions to achieve desired objectives. 
  It combines insights from descriptive and predictive analytics with mathematical optimization, simulation, and decision modeling to answer the critical question: 
  <strong>“What should we do?”</strong>. 
  This approach helps organisations allocate resources efficiently, improve operational performance, and minimize risk by suggesting the best course of action under given constraints.
</p>

<p align="center">
  In this example, prescriptive analytics is applied to workforce planning and resource allocation. 
  The analysis begins by visualising <strong>demand by shift</strong> and generating a <strong>staffing plan</strong> that ensures sufficient personnel coverage. 
  The next visual compares <strong>capacity versus required staffing</strong>, helping to identify over- or under-utilised areas. 
  A <strong>utilisation heatmap</strong> further highlights periods of inefficiency, while a <strong>cost sensitivity analysis</strong> explores the financial impact of staffing changes or scheduling adjustments. 
  Together, these visuals provide an end-to-end view of operational efficiency, cost trade-offs, and workforce optimisation.
</p>

<p align="center">
  Using Python libraries such as <code>pulp</code> or <code>ortools</code> for linear programming, prescriptive analytics models can optimise staffing schedules or production plans based on business objectives and constraints. 
  The final output, represented by the <strong>Prescriptive Print</strong>, summarises recommended actions derived from optimisation algorithms. 
  By integrating predictive insights with optimisation, prescriptive analytics empowers decision-makers to move from “What will happen?” to “What should we do about it?”, enabling data-driven strategies that maximise value and efficiency.
</p>

<p align="center">
  <strong>Why is the data below prescriptive?</strong><br>
  Descriptive analytics summarises what happened; predictive analytics estimates what will happen; prescriptive analytics recommends what to do. 
  The <code>.py</code> script I created optimises a decision (<em>staffing levels</em>) subject to goals (<em>minimise cost</em>) and constraints (<em>enough capacity to serve guests</em>). 
  The output is a concrete actionable plan — numbers of staff per shift — rather than just summaries or predictions.
</p>

---

<h2 align="center">📈 Prescriptive Analytics Python Visualisations</h2>

<p align="center">
  <img src="https://raw.githubusercontent.com/ShaheerHussain-DataScience/Shaheer-Hussain-Data-Science-Portfolio/main/Data%20Analysis%20Concepts/Prescriptive%20Analytics/01_demand_by_shift.png" alt="Demand by Shift" width="800">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/ShaheerHussain-DataScience/Shaheer-Hussain-Data-Science-Portfolio/main/Data%20Analysis%20Concepts/Prescriptive%20Analytics/02_staffing_plan.png" alt="Staffing Plan" width="800">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/ShaheerHussain-DataScience/Shaheer-Hussain-Data-Science-Portfolio/main/Data%20Analysis%20Concepts/Prescriptive%20Analytics/03_capacity_vs_required.png" alt="Capacity vs Required" width="800">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/ShaheerHussain-DataScience/Shaheer-Hussain-Data-Science-Portfolio/main/Data%20Analysis%20Concepts/Prescriptive%20Analytics/04_utilisation_heatmap.png" alt="Utilisation Heatmap" width="800">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/ShaheerHussain-DataScience/Shaheer-Hussain-Data-Science-Portfolio/main/Data%20Analysis%20Concepts/Prescriptive%20Analytics/05_cost_sensitivity.png" alt="Cost Sensitivity Analysis" width="800">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/ShaheerHussain-DataScience/Shaheer-Hussain-Data-Science-Portfolio/main/Data%20Analysis%20Concepts/Prescriptive%20Analytics/PrescriptivePrint.png" alt="Prescriptive Print Summary" width="800">
</p>

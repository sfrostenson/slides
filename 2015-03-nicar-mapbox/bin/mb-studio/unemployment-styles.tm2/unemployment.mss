#unemployment {
    line-color: #a3a3a3;
  	line-width: 0.8;
  	polygon-opacity: 0.6;
  
  [unemploy_3 = -99] { polygon-fill: #a3a3a3; }
  [unemploy_3 >= 0.9][unemploy_3 <= 5.0] { polygon-fill: #edf8fb; }
  [unemploy_3 >= 5.1][unemploy_3 <= 6.3] { polygon-fill: #b3cde3; }
  [unemploy_3 >= 6.4][unemploy_3 <= 7.5] { polygon-fill: #8c96c6; }
  [unemploy_3 >= 7.6][unemploy_3 <= 9.2] { polygon-fill: #8856a7; }
  [unemploy_3 > 9.2] { polygon-fill: #810f7c; }
}
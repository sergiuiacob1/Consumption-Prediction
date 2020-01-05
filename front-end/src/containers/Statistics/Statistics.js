import React from 'react';
import csvParser from 'papaparse';
import {
  utils,
} from '../../utils';


import {
  XYPlot,
  XAxis,
  YAxis,
  VerticalGridLines,
  HorizontalGridLines,
  VerticalBarSeries
} from 'react-vis';

export default class Statistics extends React.Component {
  constructor() {
    super();
    this.state = {
      statisticsData: {}
    };
  }

  componentDidMount() {
    fetch('https://raw.githubusercontent.com/sergiuiacob1/Consumption-Prediction/master/data/test_electricity.csv')
      .then((response) => {
        response.text().then((text) => {
          const parsedCSV = csvParser.parse(text);
          const predictModelData = utils.parseCSVData(parsedCSV);

          if (parsedCSV.errors.length) {
            alert("CSV ERRORS");
            return;
          }

          console.log(predictModelData);
          this.setState({
            statisticsData: predictModelData
          });
        });
      })
      .catch((error) => {
        console.log(error);
      });
  }

  render() {
    return ( 
    <div className = "container" >
      <div className = "row mb-3" >
        <div className = "col" >
          <XYPlot margin={{bottom: 70}} xType="ordinal" width={500} height={500}>
            <VerticalGridLines />
            <HorizontalGridLines />
            <XAxis tickLabelAngle={-45} />
            <YAxis />
            <VerticalBarSeries
              data={[
                {x: 'January', y: 10},
                {x: 'February', y: 5},
                {x: 'March', y: 15},
                {x: 'April', y: 15},
                {x: 'May', y: 15},
                {x: 'June', y: 15},
                {x: 'July', y: 15},
                {x: 'August', y: 15},
                {x: 'September', y: 15},
                {x: 'Octomber', y: 15},
                {x: 'November', y: 15},
                {x: 'December', y: 15},
              ]}
            />
          </XYPlot>
        </div> 
      </div> 
    </div >
    );
  }
}
import React from 'react';
import { fetchService } from '../../utils';
import { SingleBarChart } from './singleBarChart'
import { SingleAreaChart } from './singleAreaChart'

export default class Statistics extends React.Component {
  constructor() {
    super();
    this.state = {
      generalStatistics: {},
      monthlyStatistics: {}
    };
  }

  componentDidMount() {
    fetchService('/api/general_statistics')
      .then(response => {
        this.setState({ generalStatistics: response })
      })
    fetchService('/api/monthly_statistics')
      .then(response => {
        this.setState({ monthlyStatistics: response })
      })

  }

  renderAll() {
    const { generalStatistics } = this.state
    if (generalStatistics) {
      var statisticColumns = [];
      for (const variable in generalStatistics) {
        if (variable == "date") {
          continue
        }
        statisticColumns.push(this.renderGeneralStatisticsForKey(variable));
      }
      return statisticColumns
    }
  }

  orderStatistics() {
    var statistics = this.renderAll()
    var statisticsRow1 = [], statisticsRow2 = []
    var last = []

    for (const statistic in statistics) {
      if (statistic < 4) {
        statisticsRow1.push(statistics[statistic])
      }
      else if (statistic < 8) {
        statisticsRow2.push(statistics[statistic])
      }
      else {
        last.push(statistics[statistic])
      }
    }
    return (
      <div>
        <div className="row">
          {statisticsRow1}
        </div>
        <div className="row">
          {statisticsRow2}
        </div>
        <div className="row" style={{ margin: '0 auto', maxWidth: '25%' }}>
          {last}
        </div>
      </div>
    )

  }




  renderGeneralStatisticsForKey(key) {
    const { generalStatistics } = this.state

    if (generalStatistics[key]) {
      return (
        <div className="h-25 col">
          <h1 style={{ fontSize: '36px' }}>{key}</h1>
          <hr style={{ marginBottom: '0rem', marginTop: '0rem' }} ></hr>
          <p style={{ marginBottom: '0.5rem' }}><span style={{ fontWeight: 'bold' }}>Min: </span>{parseFloat(generalStatistics[key]["min"].toFixed(4))}</p>
          <hr style={{ marginBottom: '0rem', marginTop: '0rem' }} ></hr>
          <p style={{ marginBottom: '0.5rem' }}><span style={{ fontWeight: 'bold' }}>Max: </span>{parseFloat(generalStatistics[key]["max"].toFixed(4))}</p >
          <hr style={{ marginBottom: '0rem', marginTop: '0rem' }} ></hr>
          <p style={{ marginBottom: '0.5rem' }}><span style={{ fontWeight: 'bold' }}>Avg: </span>{parseFloat(generalStatistics[key]["avg"].toFixed(4))}</p >
          <hr style={{ marginBottom: '0rem', marginTop: '0rem' }} ></hr>
          <p style={{ marginBottom: '0.5rem' }}><span style={{ fontWeight: 'bold' }}>Sum: </span>{parseFloat(generalStatistics[key]["sum"].toFixed(4))}</p >
          <hr style={{ marginBottom: '0rem', marginTop: '0rem' }} ></hr>
          <p style={{ marginBottom: '0.5rem' }}><span style={{ fontWeight: 'bold' }}>stdDev: </span>{parseFloat(generalStatistics[key]["stdDev"].toFixed(4))}</p >
          <hr style={{ marginBottom: '0rem', marginTop: '0rem' }} ></hr>
        </div >
      )
    } else {
      return (<div>Statistics are loading..</div>)
    }
  }


  drawAllBarCharts() {
    const { monthlyStatistics } = this.state
    if (!monthlyStatistics[1]) {
      return
    }

    var singleStats = Object.keys(monthlyStatistics[1]['biomass'])

    var result = []

    for (const key in singleStats) {
      if (singleStats[key] === 'data') {
        continue;
      }
      result.push(this.drawBarChartForStat(singleStats[key]))
    }
    return result;

  }

  drawBarChartForStat(stat) {
    const { monthlyStatistics } = this.state

    if (!monthlyStatistics[1])
      return;

    const months = [" ", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const unMappedMonths = Object.keys(monthlyStatistics);
    const stats = Object.keys(monthlyStatistics[1])

    var dataRes = []

    for (const month in monthlyStatistics) {
      var obj = {}
      obj['month'] = months[parseInt(unMappedMonths[month - 1])]
      for (const keyStat in stats) {
        obj[stats[keyStat]] = monthlyStatistics[month][stats[keyStat]][stat]
      }
      // console.log(obj)s
      dataRes.push(obj)
    }

    return (<SingleBarChart data={dataRes} xAxisKey="month" statKey={stats} titleKey={stat} />)
  }

  drawAllAreaCharts(stat) {
    const { monthlyStatistics } = this.state
    if (!monthlyStatistics[1]) {
      return
    }

    var singleStats = Object.keys(monthlyStatistics[1])
    var result = []

    for (const key in singleStats) {
      result.push(this.drawAreaChartForStat(stat, singleStats[key]))
    }

    return result;
  }

  drawAreaChartForStat(stat, dataKey) {
    const { monthlyStatistics } = this.state
    if (!monthlyStatistics[1]) {
      return;
    }

    const months = [" ", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const unMappedMonths = Object.keys(monthlyStatistics);
    const stats = Object.keys(monthlyStatistics[1])

    var dataRes = []

    for (const month in monthlyStatistics) {
      var obj = {}
      obj['month'] = months[parseInt(unMappedMonths[month - 1])]
      obj['data'] = monthlyStatistics[month][dataKey][stat]
      // console.log(obj)s
      dataRes.push(obj)
    }

    return (<SingleAreaChart data={dataRes} xAxisKey="month" titleKey={dataKey} />)
  }



  render() {

    return (
      <div className="container" >

        {this.orderStatistics()}
        {this.drawAllBarCharts()}
        {this.drawAllAreaCharts('avg')}
      </div >
    );

  }
}
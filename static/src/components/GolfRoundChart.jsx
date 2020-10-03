import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';

const StatPreview = ({ active, payload, label }) => {
  if (active && payload) {
    const data = payload[0].payload;
    const fairways = data.summary.fairways;
    const greenInRegulation = data.summary.greens_in_regulation;
    const putts = data.summary.putts;
    const upAndDowns = data.summary.up_and_downs;
    const sandSaves = data.summary.sand_saves;

    return (
      <div>
        <p>{`Fairways: ${fairways}`}</p>
        <p>{`Greens In Regulation: ${greenInRegulation}`}</p>
        <p>{`Putts: ${putts}`}</p>
        <p>{`Up and Downs: ${upAndDowns}`}</p>
        <p>{`Sand Saves: ${sandSaves}`}</p>
      </div>
    );
  }

  return null;
}

const summaryStub = () => ({
    fairways: "",
    greens_in_regulation: "",
    putts: "",
    up_and_downs: "",
    sand_saves: "",
});

export const GolfRoundChart = ({ rounds, stats, statsSummary }) => {
  const roundIds = [...rounds.allIds];
  const data = roundIds.reverse().map((roundId) => {
    const round = rounds.byId[roundId];
    const summary = statsSummary.byId[roundId];
    round.summary = summary ? summary : summaryStub();
    return round;
  });

  return (
    <LineChart
      width={500}
      height={300}
      data={data}
      margin={{top: 5, right: 30, left: 10, bottom: 5}}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis
        dataKey="played_on"
        label={{value: "Played On", position: "bottom"}}
      />
      <YAxis
        label={{value: "Score", position: "insideLeft", angle: -90}}
        ticks={[70, 80, 90, 100]}
        domain={[70, 100]}
      />
      <Tooltip content={<StatPreview />} />
      <Line
        type="monotone"
        dataKey="gross_score"
        stroke="#8884d8"
        dot={true}
        activeDot={true}
      />
    </LineChart>
  );
}

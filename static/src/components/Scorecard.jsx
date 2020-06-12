import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import RoundStat from './RoundStat';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const URL_ROOT = 'http://127.0.0.1:8000';

export default function Scorecard({ round, statsByHoleId, teeBox, golfCourse, dispatch }) {
  const classes = useStyles();
  let [holes, setHoles]= useState([]);

  useEffect(() => {
    if (typeof golfCourse !== 'undefined' && typeof teeBox !== 'undefined') {
      const golfCourseId = golfCourse.id;
      const teeBoxId = teeBox.id;
      const path = `/api/golf-courses/${golfCourseId}/tee-boxes/${teeBoxId}/holes`;
      const url = new URL(path, URL_ROOT);
      axios.get(url)
        .then(res => {
          holes = res.data.result.map((hole) => ({
            holeId: hole.id,
            holeNumber: hole.hole_number,
            distance: hole.distance,
            handicap: hole.handicap,
            par: hole.par,
          }));
          setHoles(holes);
        })
        .catch(error => {
          console.log(error);
        });
    }

  }, [round.id]);

  const teeBoxInfo = () => {
    if (teeBox == undefined) return;
    return `${teeBox.tee_color} (${teeBox.course_rating} | ${teeBox.slope})`;
  }

  const frontNine = holes.slice(0,9);
  const backNine = holes.slice(9);

  let frontNinePar = 0;
  let frontNineYardage = 0;
  let backNinePar = 0;
  let backNineYardage = 0;
  frontNine.forEach((hole) => {
    frontNinePar += hole.par;
    frontNineYardage += hole.distance;
  });
  backNine.forEach((hole) => {
    backNinePar += hole.par;
    backNineYardage += hole.distance;
  });

  const frontNineScore = () => {
    let totalScore = 0;
    frontNine.forEach((hole) => {
      const holeStat = statsByHoleId[hole.holeId];
      if (typeof holeStat !== 'undefined') {
        let holeScore = holeStat.gross_score;
        totalScore += holeScore
      }
    })

    return totalScore;
  }

  const backNineScore = () => {
    let totalScore = 0;
    backNine.forEach((hole) => {
      const holeStat = statsByHoleId[hole.holeId];
      if (typeof holeStat !== 'undefined') {
        let holeScore = holeStat.gross_score;
        totalScore += holeScore
      }
    })

    return totalScore;
  }

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow key="hole_number">
            <TableCell>Hole</TableCell>
            {frontNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                {hole.holeNumber}
              </TableCell>
            ))}
            <TableCell>OUT</TableCell>
            {backNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                {hole.holeNumber}
              </TableCell>
            ))}
            <TableCell>IN</TableCell>
            <TableCell>TOT</TableCell>
          </TableRow>
          <TableRow key="distance">
            <TableCell>{teeBoxInfo()}</TableCell>
            {frontNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                {hole.distance}
              </TableCell>
            ))}
            <TableCell>{frontNineYardage}</TableCell>
            {backNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                {hole.distance}
              </TableCell>
            ))}
            <TableCell>{backNineYardage}</TableCell>
            <TableCell>
              {frontNineYardage + backNineYardage}
            </TableCell>
          </TableRow>
          <TableRow key="handicap">
            <TableCell>Handicap</TableCell>
            {frontNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                {hole.handicap}
              </TableCell>
            ))}
            <TableCell></TableCell>
            {backNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                {hole.handicap}
              </TableCell>
            ))}
            <TableCell></TableCell>
            <TableCell></TableCell>
          </TableRow>
          <TableRow key="par">
            <TableCell>Par</TableCell>
            {frontNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                {hole.par}
              </TableCell>
            ))}
            <TableCell>{frontNinePar}</TableCell>
            {backNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                {hole.par}
              </TableCell>
            ))}
            <TableCell>{backNinePar}</TableCell>
            <TableCell>
              {frontNinePar + backNinePar}
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>Score</TableCell>
            {frontNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                <RoundStat
                  round={round}
                  stat={statsByHoleId[hole.holeId]}
                  holeId={hole.holeId}
                  dispatch={dispatch}
                />
              </TableCell>
            ))}
            <TableCell>{frontNineScore()}</TableCell>
            {backNine.map((hole) => (
              <TableCell key={hole.holeNumber}>
                <RoundStat
                  round={round}
                  stat={statsByHoleId[hole.holeId]}
                  holeId={hole.holeId}
                  dispatch={dispatch}
                />
              </TableCell>
            ))}
            <TableCell>{backNineScore()}</TableCell>
            <TableCell>{frontNineScore() + backNineScore()}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
}

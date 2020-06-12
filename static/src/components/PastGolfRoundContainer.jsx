import axios from 'axios';
import { normalize, schema } from 'normalizr';
import React, { useState, useEffect }  from 'react';
import TableContainer from '@material-ui/core/TableContainer';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import PastGolfRound from './PastGolfRound';

const API_URL_ROOT = 'http://127.0.0.1:8000/api/';
const TEE_BOX_KEY = 'tee_boxes';
const GOLF_COURSE_KEY = 'golf_courses';

const teeBoxes = new schema.Entity(TEE_BOX_KEY);
const golfCourses = new schema.Entity(GOLF_COURSE_KEY, {tee_boxes: [teeBoxes]});

export default function PastGolfRoundsContainer({ rounds, stats, dispatch }) {
  const [golfCourseById, setGolfCourseById] = useState({});
  const [teeBoxById, setTeeBoxById] = useState({});
  const roundMap = rounds.byId;

  useEffect(() => {
    let mounted = true;
    if (mounted && Object.keys(roundMap).length > 0) {
      const golfCourseUrl = new URL('golf-courses', API_URL_ROOT);
      Object.keys(roundMap).map((roundId) => {
        const golfCourseId = roundMap[roundId].golf_course_id;
        golfCourseUrl.searchParams.append('id', golfCourseId);
      });
      axios.get(golfCourseUrl)
        .then(res => {
          const normalizedData = normalize(
            {GOLF_COURSE_KEY: res.data.result},
            {GOLF_COURSE_KEY: [golfCourses]}
          );
          setGolfCourseById(normalizedData.entities[GOLF_COURSE_KEY]);
          setTeeBoxById(normalizedData.entities[TEE_BOX_KEY]);
        })
        .catch(error => {
          console.log(error);
        });
    }
    return () => mounted = false;
  }, [rounds.byId]);

  const teeBox = (round) => {
    return teeBoxById[round.tee_box_id]
  }

  const golfCourse = (round) => {
    return golfCourseById[round.golf_course_id]
  }

  return (
    <React.Fragment>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Past Rounds
      </Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell />
              <TableCell>Round Id</TableCell>
              <TableCell>Played On</TableCell>
              <TableCell>Golf Course</TableCell>
              <TableCell>Tee Box</TableCell>
              <TableCell>Towards Handicap</TableCell>
              <TableCell align="right">Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.keys(roundMap).map((roundId) => (
              <PastGolfRound
                key={roundId}
                round={roundMap[roundId]}
                stats={stats}
                golfCourse={golfCourse(roundMap[roundId])}
                teeBox={teeBox(roundMap[roundId])}
                dispatch={dispatch}/>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </React.Fragment>
  );
}

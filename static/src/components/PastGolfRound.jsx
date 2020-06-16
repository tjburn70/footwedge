import React, { useState }  from 'react';
import Box from '@material-ui/core/Box';
import Collapse from '@material-ui/core/Collapse';
import IconButton from '@material-ui/core/IconButton';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import Typography from '@material-ui/core/Typography';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import Scorecard from './Scorecard';


export default function PastGolfRound({ round, stats, golfCourse, teeBox, dispatch }) {
  const [open, setOpen] = useState(false);

  const golfCourseName = () => {
    if (golfCourse === undefined) return;
    return golfCourse.name;
  }

  const teeBoxInfo = () => {
    if (teeBox === undefined) return;
    return `${teeBox.tee_color} (${teeBox.distance} | ${teeBox.course_rating})`;
  }

  const statsByHoleId = () => {
    const roundStats = round.stats.map((statId) => {
      return stats.byId[statId]
    });
    return roundStats.reduce((obj, stat, idx) => {
      return { ...obj, [stat.hole_id]: stat};
    }, {});
  }

  return (
    <React.Fragment>
        <TableRow key={round.id}>
          <TableCell>
            <IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
              {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
            </IconButton>
          </TableCell>
          <TableCell>{round.id}</TableCell>
          <TableCell>{round.played_on}</TableCell>
          <TableCell>
            {golfCourseName()}
          </TableCell>
          <TableCell>
            {teeBoxInfo()}
          </TableCell>
          <TableCell>{round.towards_handicap ? "Y" : "N"}</TableCell>
          <TableCell align="right">{round.gross_score}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
            <Collapse in={open} timeout="auto" unmountOnExit>
              <Box margin={1}>
                <Typography variant="h6" gutterBottom component="div">
                  Scorecard
                </Typography>
                <Scorecard
                  round={round}
                  statsByHoleId={statsByHoleId()}
                  teeBox={teeBox}
                  golfCourse={golfCourse}
                  dispatch={dispatch}
                />
              </Box>
            </Collapse>
          </TableCell>
        </TableRow>
    </React.Fragment>
  );
}

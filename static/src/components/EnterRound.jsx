import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Grid from '@material-ui/core/Grid';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import { MuiPickersUtilsProvider, KeyboardDatePicker } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';
import SearchBar from './SearchBar';
import { enterGolfRound } from '../actions/api';


const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
}));

const URL_ROOT = 'http://127.0.0.1:8000/api/golf-courses/';

export const EnterRound = (props) => {
  const { errorMessage } = props.data;
  const dispatch = props.dispatch;
  const [golfCourse, setGolfCourse] = useState(null);
  const [teeBoxes, setTeeBoxes] = useState([]);
  const [teeBox, setTeeBox] = useState("");
  const [roundType, setRoundType] = useState("");
  const [totalScore, setTotalScore] = useState("");
  const [towardsHandicap, setTowardsHandicap] = useState(true);
  const [playedOn, setPlayedOn] = useState(null);
  const classes = useStyles();

  useEffect(() => {
    if (golfCourse) {
      let golfCourseId = golfCourse.golf_course_id;
      let path = golfCourseId+'/tee-boxes';
      let url = URL_ROOT+path;
      axios.get(url)
        .then(res => {
          setTeeBoxes(res.data.result);
        })
        .catch(error => {
          console.log(error);
        });
    }
  }, [golfCourse]);

  const handleSubmit = (event) => {
    event.preventDefault();
    dispatch(enterGolfRound({
      golfCourseId: golfCourse.golf_course_id,
      teeBoxId: teeBox.id,
      roundType: roundType,
      totalScore: totalScore,
      towardsHandicap: towardsHandicap,
      playedOn: playedOn,
    }));
  }

  const processSearchResults = (results) => {
    const golfCourses = [];
    results.forEach(result => {
      result.golf_courses.forEach(course => {
        const golfClub = Object.assign({}, result);
        golfClub['golf_course_id'] = course.id;
        golfClub['golf_course_name'] = course.name;
        golfClub['num_holes'] = course.num_holes;
        golfCourses.push(golfClub);
      });
    });

    return golfCourses;
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          Enter a Past Round
        </Typography>

        {errorMessage &&
          <p>{errorMessage}</p>
        }

        <form
          className={classes.form}
          noValidate
          onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <FormControl className={classes.formControl}>
                <SearchBar
                  label="Search Golf Courses..."
                  targetIndex='golf_club'
                  handleSelect={(event, value) => setGolfCourse(value)}
                  processResults={(results) => processSearchResults(results)}
                />
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl className={classes.formControl}>
                <InputLabel id="tee-box-label">TeeBox</InputLabel>
                <Select
                  labelId="tee-box-label"
                  id="tee-box"
                  value={teeBox}
                  onChange={e => setTeeBox(e.target.value)}
                >
                {teeBoxes.map((box) => (
                  <MenuItem key={box.id} value={box}>
                    {box.tee_color} ({box.distance} {box.unit} | {box.course_rating})
                  </MenuItem>
                ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
                <FormControl component="fieldset">
                    <FormLabel component="legend">Round Type</FormLabel>
                      <RadioGroup
                        aria-label="roundType"
                        name="roundType"
                        onChange={e => setRoundType(e.target.value)}>
                        <FormControlLabel
                          value="18"
                          control={<Radio />}
                          label="18 Holes" />
                        <FormControlLabel
                          value="f9"
                          control={<Radio />}
                          label="Front Nine" />
                        <FormControlLabel
                          value="b9"
                          control={<Radio />}
                          label="Back Nine" />
                      </RadioGroup>
                </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                autoComplete="tscore"
                name="totalScore"
                variant="outlined"
                required
                fullWidth
                id="totalScore"
                label="Total Score"
                value={totalScore}
                onChange={e => setTotalScore(e.target.value)}
                autoFocus
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <MuiPickersUtilsProvider utils={DateFnsUtils}>
                <KeyboardDatePicker
                    disableToolbar
                    variant="inline"
                    format="MM/dd/yyyy"
                    margin="normal"
                    id="played-on"
                    label="Played On"
                    value={playedOn}
                    onChange={date => setPlayedOn(date)}
                    KeyboardButtonProps={{
                        'aria-label': 'change date',
                    }}
                />
              </MuiPickersUtilsProvider>
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={towardsHandicap}
                    onChange={e => setTowardsHandicap(e.target.checked)}
                  />
                }
                label="Towards Handicap?"
                labelPlacement="start"
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}>
            Submit
          </Button>
          <Grid container>
            <Grid item xs>
              <Link to="/player-profile" variant="body2">
                Back to Profile
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
    </Container>
  )
}

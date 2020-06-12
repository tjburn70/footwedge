import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import IconButton from "@material-ui/core/IconButton";
import EditIcon from '@material-ui/icons/Edit';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import { addRoundStat } from './actions/api';


export default function RoundStat({ round, stat, holeId, dispatch }) {
  const [open, setOpen] = React.useState(false);
  const [score, setScore] = React.useState('');
  const [fairwayHit, setFairwayHit] = React.useState(false);
  const [greenInRegulation, setGreenInRegulation] = React.useState(false);
  const [totalPutts, setTotalPutts] = React.useState('');
  const [totalChips, setTotalChips] = React.useState('');
  const [greenSideSandShots, setGreenSideSandShots] = React.useState(null);
  const [totalPenalties, setTotalPenalties] = React.useState('');

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const submitStat = () => {
    const data = {
      score: score,
      fairwayHit: fairwayHit,
      greenInRegulation: greenInRegulation,
      totalPutts: totalPutts,
      totalChips: totalChips,
      greenSideSandShots: greenSideSandShots,
      totalPenalties: totalPenalties,
    };
    dispatch(addRoundStat(round.user_id, round.id, holeId, data));
    setOpen(false);
  }

  const display = () => {
    if (typeof stat !== 'undefined') {
      return (
        <Button onClick={handleClickOpen} size='small'>
          {stat.gross_score}
        </Button>
      );
    } else {
      return (
        <IconButton onClick={handleClickOpen}>
          <EditIcon />
        </IconButton>
      );
    }
  }

  return (
    <div>
      {display()}
      <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title">Round Stats</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            id="score"
            label="Score"
            value={score}
            onChange={e => setScore(e.target.value)}
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={fairwayHit}
                onChange={e => setFairwayHit(e.target.checked)}
              />
            }
            label="Fairway Hit"
            labelPlacement="start"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={greenInRegulation}
                onChange={e => setGreenInRegulation(e.target.checked)}
              />
            }
            label="Green In Regulation"
            labelPlacement="start"
          />
          <TextField
            margin="dense"
            id="putts"
            label="Putts"
            value={totalPutts}
            onChange={e => setTotalPutts(e.target.value)}
          />
          <TextField
            margin="dense"
            id="chips"
            label="Chips"
            onChange={e => setTotalChips(e.target.value)}
          />
          <TextField
            margin="dense"
            id="greenSideSandShots"
            label="Greenside Sand Shots"
            onChange={e => setGreenSideSandShots(e.target.value)}
          />
          <TextField
            margin="dense"
            id="penalties"
            label="Penalties"
            onChange={e => setTotalPenalties(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button color="primary" onClick={submitStat}>
            Enter
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

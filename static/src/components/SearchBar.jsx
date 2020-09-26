import _ from 'lodash';
import axios from 'axios';
import React from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import CircularProgress from '@material-ui/core/CircularProgress';

function sleep(delay = 0) {
  return new Promise((resolve) => {
    setTimeout(resolve, delay);
  });
}

const SEARCH_API_BASE_URL = 'http://0.0.0.0:8001';

export default function SearchBar({ label, targetIndex, handleSelect, processResults }) {
  const path = ''.concat('/', targetIndex);
  const url = new URL(path, SEARCH_API_BASE_URL);
  url.searchParams.append('query_type', 'wildcard');
  url.searchParams.append('field', 'name');
  const [open, setOpen] = React.useState(false);
  const [options, setOptions] = React.useState([]);
  const loading = open && options.length === 0;

  React.useEffect(() => {
    let active = true;

    if (!loading) {
      return undefined;
    }

    return () => {
      active = false;
    };
  }, [loading]);

  React.useEffect(() => {
    if (!open) {
      setOptions([]);
    }
  }, [open]);

  const handleSearchChange = (event, value) => {
    setTimeout(() => {
      if (value.length < 1) return;
      url.searchParams.set('q', value);
        axios.get(url)
          .then(res => {
            let searchResults = res.data.hits;
            let results = searchResults.map(result => (
              result._source
            ));
            const processedResults = processResults(results);
            setOptions(processedResults);
          })
          .catch(error => {
            console.log(error);
          });
    }, 300);
  }

  return (
    <Autocomplete
      id="search-bar"
      style={{ width: 300 }}
      open={open}
      onOpen={() => {
        setOpen(true);
      }}
      onClose={() => {
        setOpen(false);
      }}
      onInputChange={_.debounce(
        (event, value) => handleSearchChange(event, value),
        500,
        {leading: true}
      )}
      onChange={handleSelect}
      filterOptions={(options) => options}
      getOptionLabel={(option) => option.golf_course_name}
      getOptionSelected={(option, value) => option.name === value.name}
      groupBy={(option) => option.name}
      options={options}
      loading={loading}
      renderInput={(params) => (
        <TextField
          {...params}
          label={label}
          variant="outlined"
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <React.Fragment>
                {loading ? <CircularProgress color="inherit" size={20} /> : null}
                {params.InputProps.endAdornment}
              </React.Fragment>
            ),
          }}
        />
      )}
    />
  );
}

import React, { useState } from "react";
import "./SearchBar.css";
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
function List({list}) {
  if (!list) {
    return null;
  }
  if (list == -1) {
    return <p>No document found</p>
  }
  return (
    <div className="scrollable-div">
    <ul>
      {list.map(item => (
          <Item key={item.id} item={item} />
      ))}
    </ul>
    </div>
  );
}
function Item({item}) {
  return (
    <li>
      {item}
    </li>
  );
}
function loadingBar() {
  return (
    <Box sx={{ display: 'flex' }}>
      <CircularProgress />
    </Box>
  );
}
function SearchBar({ placeholder}) {
  const [query, setquery] = useState("");
  const [docs, setdocs] = useState("");
  const[loading, setloading] = useState(false);

  const handletextChange = (event) => {
    const searchWord = event.target.value;
    setquery(searchWord);
  };

  const clearInput = () => {
    setquery("");
  };

  const onFormSubmit = e => {
    e.preventDefault();
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query})
    };
    // console.log(requestOptions)
    setloading(true)
    fetch('http://127.0.0.1:5000/query', requestOptions)
        .then(response => response.json())
        .then(data => setdocs(data));
      console.log(docs)
      setloading(false)
  }
  if (loading) {
    return (<div style={{margin:"50%"}}> <CircularProgress /> </div>);
  }
  else {
    return (
      <div>
        <div className="search">
          <div className="searchInputs">
            <form onSubmit={e => { onFormSubmit(e) }}>
              <input type="text" placeholder={placeholder} value={query} onChange={handletextChange}/>
              <Button variant="contained" type ="submit">Submit</Button>
            </form>
          </div>
        </div>

        <div>
          <h3> documents using BM 25 </h3>
            <List list={docs['bm_25']} />
        </div>
        <div>
          <h3> documents using vector space model </h3>
          <List list={docs['vsm']}/>
        </div>
      </div>
  );
}
}

export default SearchBar;

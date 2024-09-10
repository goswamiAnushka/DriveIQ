import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Dashboard from './components/Dashboard/Dashboard';
import Journey from './components/Journey/Journey';
import Login from './components/Login/Login';
import './styles/styles.scss';

function App() {
    return (
        <Router>
            <Navbar />
            <Switch>
                <Route path="/dashboard" component={Dashboard} />
                <Route path="/journey" component={Journey} />
                <Route path="/login" component={Login} />
                <Route path="/" exact component={Login} />
            </Switch>
        </Router>
    );
}

export default App;

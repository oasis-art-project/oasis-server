import React from "react";
import { Route, Switch } from "react-router-dom";
import Home from "./containers/Home";
import NotFound from "./containers/NotFound"
import Login from "./containers/Login";
import ArtistDetails from "./containers/ArtistDetails"
import PlaceDetails from "./containers/PlaceDetails"

export default () =>
    <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/login" exact component={Login} />
        <Route path="/ArtistDetails" component={ArtistDetails} />
        <Route path="/PlaceDetails" component={PlaceDetails} />
        {/*Catch all unmatched routes and redirected to 404*/}
        <Route component={NotFound} />


    </Switch>;
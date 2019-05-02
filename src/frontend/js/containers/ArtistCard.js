import React, {Component} from "react";
import {Card, CardBody, CardImg, CardSubtitle, CardText, CardTitle} from "reactstrap";
import {Button} from "reactstrap";
import oasis_logo from './assets/oasis_logo.png';
import CardHeader from "reactstrap/es/CardHeader";
import "./ArtistCard.css";

class ArtistCard extends Component {
	render() {
        let { id, artistName, genres, description } = this.props.artist;
        return (
            <div>
                <Card className="card-body">
                    <CardHeader>{artistName}</CardHeader>
                    <CardImg top width="50%" src={oasis_logo} alt="Card image cap" /> // get artist picture here
                    <CardBody>
                        <CardTitle>{genres}</CardTitle>
                        <CardSubtitle>{location}</CardSubtitle>
                        <CardText>{description}</CardText>
                        <Button color="primary" size="sm" href="#">Contact</Button>
                    </CardBody>
                </Card>
            </div>
        )
    }
}

export default ArtistCard;
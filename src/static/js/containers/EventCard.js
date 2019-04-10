import React, {Component} from "react";
import {Card, CardBody, CardImg, CardSubtitle, CardText, CardTitle} from "reactstrap";
import {Button} from "reactstrap";
import oasis_logo from './assets/oasis_logo.png';
import CardHeader from "reactstrap/es/CardHeader";
import "./EventCard.css";



class EventCard extends Component {


    render() {
        let { id, eventStatus, eventTitle, eventDate, eventDetails } = this.props.event;
        return (
            <div>
                <Card className="card-body">
                    <CardHeader>{eventStatus}</CardHeader>
                    <CardImg top width="50%" src={oasis_logo} alt="Card image cap" />
                    <CardBody>
                        <CardTitle>{eventTitle}</CardTitle>
                        <CardSubtitle>{eventDate}</CardSubtitle>
                        <CardText>{eventDetails}</CardText>
                        <Button color="primary" size="sm" href="/events">Details</Button>
                    </CardBody>
                </Card>
            </div>
        )
    }

}

export default EventCard;

import React, { Component } from "react";
import "./Home.css";
import EventCard from './EventCard';
import {Container} from "reactstrap";
import {Row} from "react-bootstrap";
import {Col} from "react-bootstrap";



class Home extends Component {
    constructor(){
        super();
        this.state = {
            events: [
                {
                    eventTitle: "Art New Years Party",
                    eventDate: "01/01/2020",
                    eventDetails: "Come have fun with us for New Years!"

                },
                {
                    eventTitle: "Art New Years Party 2",
                    eventDate: "01/01/2021",
                    eventDetails: "Come have fun with us for New Years, Again!"

                },
                {
                    eventTitle: "Art New Years Party 3",
                    eventDate: "01/01/2022",
                    eventDetails: "Come have fun with us for New Years, Yet Again!"

                },
                {
                    eventTitle: "Art New Years Party 4",
                    eventDate: "01/01/2023",
                    eventDetails: "The party just keeps going!"

                }

            ]
        }
    }
    render() {
        let EventCards = this.state.events.map(event => {
            return(
                <Col sm="3">
                    <EventCard event={event.eventTitle}/>
                </Col>
            )
        });
        return (
            <Container>
                <Row>
                    {EventCards}
                </Row>
            </Container>
        );
    }
}

export default Home;


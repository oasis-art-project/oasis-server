import React, { Component } from "react";
import "./Home.css";
import EventCard from './EventCard';
import {Container, Row, Col} from "reactstrap";



class Home extends Component {
    constructor(){
        super();
        this.state = {
            events: [
                {
                    id: 1,
                    eventStatus: "Past Event",
                    eventTitle: "Art New Years Party",
                    eventDate: "01/01/2019",
                    eventDetails: "Come have fun with us for New Years!"

                },
                {
                    id: 2,
                    eventStatus: "Upcoming Event",
                    eventTitle: "Art New Years Party 2",
                    eventDate: "01/01/2020",
                    eventDetails: "Come have fun with us for New Years, Again!"

                },
                {
                    id: 3,
                    eventStatus: "Upcoming Event",
                    eventTitle: "Art New Years Party 3",
                    eventDate: "01/01/2021",
                    eventDetails: "Come have fun with us for New Years, Yet Again!"

                },
                {
                    id: 4,
                    eventStatus: "Upcoming Event",
                    eventTitle: "Art New Years Party 4",
                    eventDate: "01/01/2022",
                    eventDetails: "The party just keeps going!"

                },
                {
                    id: 5,
                    eventStatus: "Upcoming Event",
                    eventTitle: "Art New Years Party 5",
                    eventDate: "01/01/2023",
                    eventDetails: "Phew, it never ends!"

                },
                {
                    id: 6,
                    eventStatus: "Upcoming Event",
                    eventTitle: "Art New Years Party 5",
                    eventDate: "01/01/2024",
                    eventDetails: "Phew, it never ends!"
                }

            ]
        }
    }

    render() {
        let EventCards = this.state.events.map(event => {
            return(
                <Col sm="4">
                    <EventCard key={event.id} event={event} />
                </Col>
            )
        });
        return (
            <Container fluid>
                <Row>
                    {EventCards}
                </Row>
            </Container>
        );
    }
}

export default Home;
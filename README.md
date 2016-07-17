# Design Space Generator

One of the components of Hesperus, the design space generator runs a small flask server in a Docker container, consumes a JSON description of the design space.  It then responds to get requests with JSON documents describing individual designs.

Endpoints:
/space [PUT]: recieves a JSON docuemnt, desciribng the combinatory tree and leaf nodes that produce the space
/stats [GET]: returns basic stats on current status: size of space, current progress through space
/design [GET]: returns a JSON document that describes a design.  Returns the next sequentially.  If all designs have been dispatched, returns 404
/design/[int] [GET]:

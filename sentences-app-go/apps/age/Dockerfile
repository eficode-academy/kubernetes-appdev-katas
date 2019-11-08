FROM golang:alpine AS builder
WORKDIR $GOPATH/src/mypackage/myapp/
ADD age.go .

RUN apk update && apk add --no-cache git
RUN go get -d -v
RUN CGO_ENABLED=0 GOOS=linux go build -o /go/bin/goapp

RUN adduser -S scratchuser
RUN chown scratchuser /go/bin/goapp

FROM scratch
COPY --from=builder /go/bin/goapp /goapp
COPY --from=builder /etc/passwd /etc/passwd
USER scratchuser
CMD ["/goapp"]

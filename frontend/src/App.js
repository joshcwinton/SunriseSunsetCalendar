import ZipForm from "./components/ZipForm";

function App() {
  return (
    <div className="App">
      <h1>Sunrise Sunset Calendar Generator</h1>
      <p>
        This website creates a .ics file which can be opened in a calendar
        client. The file will add events for sunsrise and sunset in the location
        that you provide in the local time zone of your computer.
      </p>

      <ZipForm />

      <p>
        Sunrise and sunset times are from{" "}
        <a href="https://api.sunrise-sunset.org/json">
          Sunrise Sunset Calendar API
        </a>
        .
      </p>
      <a href="https://github.com/joshcwinton/SunriseSunsetCalendar">
        Source Code
      </a>
    </div>
  );
}

export default App;

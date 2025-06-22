import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:intl/intl.dart';

import 'package:snacktrac/ui/past_summary/widgets/past_summary_screen.dart';

class ArchivePage extends StatefulWidget {
  const ArchivePage({super.key});

  @override
  State<ArchivePage> createState() => _ArchivePageState();
}


class _ArchivePageState extends State<ArchivePage> {
  CalendarFormat format = CalendarFormat.month;
  DateTime _focusedDay = DateTime.now();
  DateTime? _chosenDate;
  String dateString = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold (
      appBar: AppBar(title: const Text('Find a Past Report:', 
        style: TextStyle(color: Colors.white)), backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            const SizedBox(height:30),
            TableCalendar(
              headerStyle: HeaderStyle(
                formatButtonVisible: false,
              ),
              calendarFormat: format,
              focusedDay: _focusedDay,
              firstDay: DateTime.utc(2025, 6, 22),
              lastDay: DateTime.utc(2050, 6, 22),
              selectedDayPredicate: (date) {
                return isSameDay(_chosenDate, date);
              },
              onDaySelected: (chosenDate, focusedDay) {
                setState(() {
                  _chosenDate = chosenDate;
                  _focusedDay = focusedDay;
                  dateString =  DateFormat('MMMM d, y').format(chosenDate);
                });
              }, 
              onPageChanged: (focusedDay) {
                _focusedDay = focusedDay;
              },
            ),
            const SizedBox(height:60),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => PastSummaryPage(dateString: dateString)),
                );
              }, 
              child: Padding(
                padding: const EdgeInsets.all(15.0),
                child: const Text('Get report'),
              ),
            ),
          ],
        )
      )
    );

  }

}



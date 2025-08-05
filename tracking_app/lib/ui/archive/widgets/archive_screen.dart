import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/global.dart';
import 'package:Snacked/ui/archive/view_model/archive_vm.dart';


class ArchivePage extends StatefulWidget {
  const ArchivePage({super.key, required this.viewModel});
  final ArchiveViewModel viewModel;

  @override
  State<ArchivePage> createState() => _ArchivePageState();
}


class _ArchivePageState extends State<ArchivePage> {
  CalendarFormat format = CalendarFormat.month;
  DateTime _focusedDay = DateTime.now();
  DateTime? _chosenDate;
  Set<DateTime> daysToHighlight = {};

  @override
  void initState() {
    super.initState();
    highlightedDays();
  }

  Future<void> highlightedDays() async {
    await storeRepo.fetchUserData(authRepo.userID);
    final Set<String> dates = storeRepo.data.map((x) => x['date'] as String).toSet();

    DateTime startDay = DateTime.utc(2025, 6, 22);
    while(!isSameDay(startDay, DateTime.now())) {
      String current = DateFormat('yyyyMMdd').format(startDay);
      if(dates.contains(current)) {
        daysToHighlight.add(startDay);
      }
      startDay = startDay.add(Duration(days:1));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold (
      appBar: AppBar(title: const Text('Find a Past Report:', 
        style: TextStyle(color: Colors.white)), backgroundColor: Colors.black, 
        automaticallyImplyLeading:false),
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
              calendarBuilders: CalendarBuilders(
                defaultBuilder: (context, day, focusedDay) {
                  final highlight = daysToHighlight.any((x) => isSameDay(x, day));
                  if(highlight) {
                    return Center(
                      child: Text(
                        '${day.day}',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Colors.orange,
                        ),
                      ),
                    );
                    // return Container(
                    //   decoration: BoxDecoration(
                    //     color: Colors.orange,
                    //     shape: BoxShape.circle,
                    //   )
                    // );
                  }
                }
              ), 
              selectedDayPredicate: (date) {
                return isSameDay(_chosenDate, date);
              },
              onDaySelected: (chosenDate, focusedDay) {
                setState(() {
                  _chosenDate = chosenDate;
                  _focusedDay = focusedDay;
                  widget.viewModel.setDate(chosenDate);
                });
              }, 
              onPageChanged: (focusedDay) {
                _focusedDay = focusedDay;
              },
            ),
            const SizedBox(height:60),
            FilledButton(
              onPressed: () async {
                if (await widget.viewModel.getFromStorage()) {
                  context.go('/archive/pastReport');
                } else { context.go('/archive/notFound'); }
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



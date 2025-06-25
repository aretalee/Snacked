import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../data/repositories/auth_repository.dart';

import '../ui/archive/widgets/archive_screen.dart';
import '../ui/change_password/widgets/change_password_screen.dart';
import '../ui/change_password/view_model/change_password_vm.dart';
import '../ui/change_username/widgets/change_username_screen.dart';
import '../ui/change_username/view_model/change_username_vm.dart';
import '../ui/export_data/widgets/export_screen.dart';
import '../ui/info/widgets/info_screen.dart';
import '../ui/login/widgets/login_screen.dart';
import '../ui/login/view_model/login_vm.dart';
import '../ui/navigation_bar/widgets/navigation_bar.dart';
import '../ui/navigation_bar/view_model/navigation_bar_vm.dart';
import '../ui/past_summary/widgets/past_summary_screen.dart';
import '../ui/profile/widgets/profile_screen.dart';
import '../ui/profile/view_model/profile_vm.dart';
import '../ui/set_goals/widgets/set_goals_screen.dart';
import '../ui/sign_in_prompt/widgets/sign_in_prompt_screen.dart';
import '../ui/signup/widgets/sign_up_screen.dart';
import '../ui/signup/view_model/sign_up_vm.dart';
import '../ui/summary/widgets/summary_screen.dart';
import '../ui/summary/widgets/no_data_screen.dart';
import '../ui/summary/widgets/prompt_screen.dart';

final GlobalKey<NavigatorState> _rootNavigatorKey = GlobalKey<NavigatorState>(debugLabel: 'root');
final GlobalKey<NavigatorState> _shellNavigatorKey = GlobalKey<NavigatorState>(debugLabel: 'shell');


GoRouter router(AuthRepository auth) => GoRouter(
  initialLocation: '/summary',
  navigatorKey: _rootNavigatorKey,
  redirect: (context, state) {
    final user = auth.currentUser;
    final loggingIn = state.matchedLocation == '/login';
    print(state.matchedLocation);
    if (user == null && (state.matchedLocation != '/signin' && state.matchedLocation != '/signin/signup' && state.matchedLocation != '/signin/login')) {
      return '/signin';
    }
    else if (loggingIn) {
      return '/summary';
    }
    return null;
  },
  routes: [
    // GoRoute(
    //   path: '/',
    //   builder: (context, state) => NavBar(viewModel: NavBarViewModel()),
    //   routes: [
    //     GoRoute(
    //       path: 'noData',
    //       builder: (context, state) => NoDataSummary(),
    //     ),
    //     GoRoute(
    //       path: 'prompt',
    //       builder: (context, state) => PromptPage(),
    //     ),
    //   ]
    // ),
    ShellRoute(
      navigatorKey: _shellNavigatorKey,
      builder: (context, state, child) {
        return NavBar(viewModel: NavBarViewModel(), child: child);
      },
      routes: [
        GoRoute(
          path: '/summary',
          builder: (context, state) => SummaryPage(),
          routes: [
            // need to write in logic here
            GoRoute(
              path: 'noData',
              builder: (context, state) => NoDataSummary(),
            ),
            GoRoute(
              path: 'prompt',
              builder: (context, state) => PromptPage(),
            ),
          ]
        ),
        GoRoute(
          path: '/archive',
          builder: (context, state) => ArchivePage(),
          routes: [
            GoRoute(
              path: 'pastReport',
              builder: (context, state) => PastSummaryPage(date: DateTime.now()),
            ),
          ]
        ),
        GoRoute(
          path: '/profile',
          builder: (context, state) => ProfilePage(viewModel: ProfileViewModel()),
          routes: [
            GoRoute(
              path: 'setGoals',
              builder: (context, state) => SetGoalsPage(),
            ),
            GoRoute(
              path: 'export',
              builder: (context, state) => ExportPage(),
            ),
            GoRoute(
              path: 'changeUsername',
              builder: (context, state) => ChangeNamePage(viewModel: ChangeNameViewModel()),
            ),
            GoRoute(
              path: 'changePassword',
              builder: (context, state) => ChangePwdPage(viewModel: ChangePwdViewModel()),
            ),
            GoRoute(
              path: 'info',
              builder: (context, state) => InfoPage(),
            ),
            GoRoute(
              path: 'signOut',
              builder: (context, state) => SignInPage(),
            ),
          ]
        ),
      ]
    ),
    // GoRoute(
    //   path: '/',
    //   builder: (context, state) => SummaryPage(),
    //   routes: [
    //     GoRoute(
    //       path: 'noData',
    //       builder: (context, state) => NoDataSummary(),
    //     ),
    //     GoRoute(
    //       path: 'prompt',
    //       builder: (context, state) => PromptPage(),
    //     ),
    //   ]
    // ),
    GoRoute(
      path: '/signin',
      builder: (context, state) => SignInPage(),
      routes: [
        GoRoute(
          path: 'signup',
          builder: (context, state) => SignUpPage(viewModel: SignUpViewModel()),
        ),
        GoRoute(
          path: 'login',
          builder: (context, state) => LoginPage(viewModel: LoginViewModel()),
        ),
      ]
    ),
    // GoRoute(
    //   path: '/summary',
    //   builder: (context, state) => SummaryPage(),
    // ),
    // GoRoute(
    //   path: '/archive',
    //   builder: (context, state) => ArchivePage(),
    //   routes: [
    //     GoRoute(
    //       path: 'pastReport',
    //       builder: (context, state) => PastSummaryPage(date: DateTime.now()),
    //     ),
    //   ]
    // ),
    // GoRoute(
    //   path: '/profile',
    //   builder: (context, state) => ProfilePage(viewModel: ProfileViewModel()),
    //   routes: [
    //     GoRoute(
    //       path: 'setGoal',
    //       builder: (context, state) => SetGoalsPage(),
    //     ),
    //     GoRoute(
    //       path: 'export',
    //       builder: (context, state) => ExportPage(),
    //     ),
    //     GoRoute(
    //       path: 'changeUsername',
    //       builder: (context, state) => ChangeNamePage(viewModel: ChangeNameViewModel()),
    //     ),
    //     GoRoute(
    //       path: 'changePassword',
    //       builder: (context, state) => ChangePwdPage(viewModel: ChangePwdViewModel()),
    //     ),
    //     GoRoute(
    //       path: 'info',
    //       builder: (context, state) => InfoPage(),
    //     ),
    //     GoRoute(
    //       path: 'signOut',
    //       builder: (context, state) => SignInPage(),
    //     ),
    //   ]
    // ),
  ]
);




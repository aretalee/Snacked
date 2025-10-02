import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../data/repositories/auth_repository.dart';
import '../ui/archive/widgets/archive_screen.dart';
import '../ui/archive/widgets/not_found_screen.dart';
import '../ui/archive/view_model/archive_vm.dart';
import '../ui/change_password/widgets/change_password_screen.dart';
import '../ui/change_password/view_model/change_password_vm.dart';
import '../ui/change_username/widgets/change_username_screen.dart';
import '../ui/change_username/view_model/change_username_vm.dart';
import '../ui/export_data/widgets/export_screen.dart';
import '../ui/export_data/view_model/export_vm.dart';
import '../ui/info/widgets/info_screen.dart';
import '../ui/login/widgets/login_screen.dart';
import '../ui/login/view_model/login_vm.dart';
import '../ui/navigation_bar/widgets/navigation_bar.dart';
import '../ui/navigation_bar/view_model/navigation_bar_vm.dart';
import '../ui/archive/widgets/past_summary_screen.dart';
import '../ui/profile/widgets/profile_screen.dart';
import '../ui/profile/view_model/profile_vm.dart';
import '../ui/set_goals/widgets/set_goals_screen.dart';
import '../ui/set_goals/view_model/set_goals_vm.dart';
import '../ui/sign_in_prompt/widgets/sign_in_prompt_screen.dart';
import '../ui/signup/widgets/sign_up_screen.dart';
import '../ui/signup/view_model/sign_up_vm.dart';
import '../ui/summary/widgets/home_screen.dart';
import '../ui/summary/widgets/summary_screen.dart';
import '../ui/summary/widgets/no_data_screen.dart';
import '../ui/summary/widgets/comment_screen.dart';
import '../ui/summary/view_model/summary_vm.dart';
import '../ui/auth/view_model/auth_vm.dart';

final GlobalKey<NavigatorState> _rootNavigatorKey = GlobalKey<NavigatorState>(debugLabel: 'root');
final GlobalKey<NavigatorState> _shellNavigatorKey = GlobalKey<NavigatorState>(debugLabel: 'shell');
final authVM = AuthViewModel();
final summaryVM = SummaryViewModel();
final archiveVM = ArchiveViewModel();

GoRouter router(AuthRepository auth) => GoRouter(
  initialLocation: '/home',
  navigatorKey: _rootNavigatorKey,
  refreshListenable: authVM,
  redirect: (context, state) async {
    if (!authVM.initialized) { return null; }
    if (!authVM.loggedIn && (state.matchedLocation != '/signin' && state.matchedLocation != '/signin/signup' && state.matchedLocation != '/signin/login')) {
      return '/signin';
    } 
    return null;
  },
  routes: [
    ShellRoute(
      navigatorKey: _shellNavigatorKey,
      builder: (context, state, child) {
        return NavBar(viewModel: NavBarViewModel(), where: state.matchedLocation, child: child);
      },
      routes: [
        GoRoute(
          path: '/home',
          builder: (context, state) => HomePage(viewModel: summaryVM, viewModelA: archiveVM),
          routes: [
            GoRoute(
              path: 'summary',
              builder: (context, state) => SummaryPage(viewModel: summaryVM, viewModelA: archiveVM),
            ),
            GoRoute(
              path: 'noData',
              builder: (context, state) => NoDataSummary(),
            ),
            GoRoute(
              path: 'comments',
              builder: (context, state) => CommentPage(viewModel: summaryVM),
            ),
          ]
        ),
        GoRoute(
          path: '/archive',
          builder: (context, state) => ArchivePage(viewModel: archiveVM),
          routes: [
            GoRoute(
              path: 'pastReport',
              builder: (context, state) => PastSummaryPage(viewModel: archiveVM),
            ),
            GoRoute(
              path: 'notFound',
              builder: (context, state) => NotFoundPage(viewModel: archiveVM),
            ),
          ]
        ),
        GoRoute(
          path: '/profile',
          builder: (context, state) => ProfilePage(viewModel: ProfileViewModel()),
          routes: [
            GoRoute(
              path: 'setGoals',
              builder: (context, state) => SetGoalsPage(viewModel: SetGoalsViewModel()),
            ),
            GoRoute(
              path: 'export',
              builder: (context, state) => ExportPage(viewModel: ExportViewModel()),
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
  ]
);



